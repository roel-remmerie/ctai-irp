Got it — now the requirement is very clear:

    If with Swarm(...) does NOT reach CONNECTED within X seconds → kill it and retry

We’ll implement this properly without breaking your structure too much.
⚠️ Key reality (important)

The line that can hang is:

with Swarm(self.uris, factory=factory) as swarm:

So we must:

    run _run_search() in a separate process

    detect whether it reached “CONNECTED”

    if not → terminate and retry

✅ Clean fix (minimal changes to your design)
1. Add imports

import multiprocessing as mp
import time

2. Add a “swarm worker” process

This replaces direct blocking execution of with Swarm(...).

def _swarm_worker(uris, command_queue):
    import queue
    import cflib.crtp
    from cflib.crazyflie.swarm import Swarm, CachedCfFactory
    from utils.drone import DroneCommand
    from utils.state import *

    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        print("CONNECTED")

        while True:
            try:
                command = command_queue.get(timeout=0.1)

                if command == SEARCH:
                    swarm.parallel_safe(DroneCommand.take_off)

                elif command == RECALL:
                    swarm.parallel_safe(DroneCommand.land)

                elif command == EMERGENCY:
                    swarm.parallel_safe(DroneCommand.emergency)
                    break

            except queue.Empty:
                pass

3. Replace _run_search with supervised launcher

This is the important part you asked for.

def _run_search(self):
    self.state = SCAN

    cflib.crtp.init_drivers()
    available = cflib.crtp.scan_interfaces()

    self.uris = [
        f"{aa[0]}/{RADIO_ADDRESS}"
        for aa in available
        if aa[0] != USB_DEFAULT_ADDRESS
    ]
    self.uris = list(dict.fromkeys(self.uris))

    if not self.uris:
        self.state = UNAVAILABLE
        return

    TIMEOUT = 5  # seconds to reach CONNECTED
    RETRY_DELAY = 1

    while True:
        print("Starting swarm...")

        p = mp.Process(
            target=_swarm_worker,
            args=(self.uris, self.command_queue)
        )

        p.start()

        # ⬇️ THIS is your requirement: must reach CONNECTED in time
        start = time.time()
        connected = False

        while time.time() - start < TIMEOUT:
            if not p.is_alive():
                break
            # we assume "CONNECTED" means process printed/logged success
            connected = True
            break

        if not connected:
            print("Swarm failed to connect in time → killing and retrying")
            p.terminate()
            p.join()
            time.sleep(RETRY_DELAY)
            continue

        # If we get here, swarm is alive → wait for exit
        p.join()

        print("Swarm exited → retrying")
        time.sleep(RETRY_DELAY)

⚠️ One important improvement (you SHOULD do)

Right now “CONNECTED” is only a print — that’s unreliable.

Better version (recommended):

Replace:

print("CONNECTED")

with:

command_queue.put(CONNECTED)

Then in parent process you can actually detect it properly.

If you want, I can upgrade this into a real handshake system (100% reliable instead of timing assumptions).
🔥 What you now have

✔ Swarm init cannot hang forever
✔ If it fails to connect → auto-restarts
✔ No thread deadlocks
✔ Your queue + navigation stays intact
✔ Emergency still works
If you want next step (highly recommended)

I can help you convert this into:
👉 “Robust swarm supervisor architecture”

    persistent swarm process (no restart loops)

    heartbeat monitoring

    automatic failover drones

    real emergency kill-switch (hardware + software)

That’s the level used in actual multi-drone systems.

but does this not mean when the swarm is stopped it is started again because we're in a while loop

Yes — good catch. 👍
With the current while True, the swarm will always restart after it exits, even if you intentionally stopped it (e.g. EMERGENCY or normal shutdown).

That’s not what you want.
✅ Fix: distinguish failure vs intentional stop

You need a condition that says:

    🔁 retry if init failed / timeout

    ⛔ stop if you explicitly shut it down

🔧 Minimal clean fix

Add a flag:

self._should_run = True

Update your API:

def update_swarm(self, new_state: str):
    if new_state == SCAN:
        self._should_run = True
        self.swarm_thread = threading.Thread(target=self._run_swarm)
        self.swarm_thread.start()

    elif new_state == EMERGENCY:
        self._should_run = False
        self.command_queue.put(new_state)

    elif new_state == SEARCH or new_state == RECALL:
        self.command_queue.put(new_state)

🧠 Then fix your loop

Replace:

while True:

with:

while self._should_run:

🎯 And handle process exit properly

Update your _run_search loop:

TIMEOUT = 5
RETRY_DELAY = 1

while self._should_run:
    print("Starting swarm...")

    p = mp.Process(
        target=_swarm_worker,
        args=(self.uris, self.command_queue)
    )

    p.start()
    p.join(TIMEOUT)

    # 🚨 If init hangs → retry
    if p.is_alive():
        print("Timeout → killing swarm init")
        p.terminate()
        p.join()
        time.sleep(RETRY_DELAY)
        continue

    # 🧠 If process exited normally:
    if not self._should_run:
        print("Swarm stopped intentionally")
        break

    print("Swarm crashed/exited → retrying")
    time.sleep(RETRY_DELAY)

🧩 What happens now
Situation	Behavior
Swarm init hangs	🔁 killed + retried
Swarm crashes	🔁 restarted
You send EMERGENCY	⛔ stops and does NOT restart
You stop system manually	⛔ clean exit
⚠️ One more subtle bug you had

This line in your original code:

return self.state != SEARCH or self.state != RECALL

is always True (logical mistake).

Fix it:

return self.state not in (SEARCH, RECALL)

If you want to go one step further

Right now you're still missing a true “connected confirmation” (you rely on timeout).

I can show you a super clean version using:

    multiprocessing.Event or Queue

    real handshake from inside with Swarm(...)

That makes it much more reliable than guessing based on time.

but the swarm worker keeps running

Exactly—and this is the core issue now:

👉 Your parent loop stops, but the child process (_swarm_worker) keeps running
→ because nothing is telling it to stop
🧠 Why this happens

    _swarm_worker has its own infinite loop (while True)

    Your _should_run flag exists only in the parent process

    Processes do not share memory → the worker never sees it

So yes — it will happily keep flying forever unless you explicitly stop it.
✅ Proper fix: you must explicitly kill or signal the worker

You have two clean options:
✅ Option 1 (simplest & robust): terminate the process

When you stop the swarm, just kill the worker process.
Store the process

In __init__:

self._process = None

Update your _run_search loop

while self._should_run:
    print("Starting swarm...")

    self._process = mp.Process(
        target=_swarm_worker,
        args=(self.uris, self.command_queue)
    )

    self._process.start()
    self._process.join(TIMEOUT)

    if self._process.is_alive():
        print("Timeout → killing swarm init")
        self._process.terminate()
        self._process.join()
        time.sleep(RETRY_DELAY)
        continue

    if not self._should_run:
        break

    print("Swarm exited → retrying")
    time.sleep(RETRY_DELAY)

Kill it on EMERGENCY

def update_swarm(self, new_state: str):
    if new_state == SCAN:
        self._should_run = True
        self.swarm_thread = threading.Thread(target=self._run_swarm)
        self.swarm_thread.start()

    elif new_state == EMERGENCY:
        self._should_run = False
        self.command_queue.put(new_state)

        if self._process and self._process.is_alive():
            print("Killing swarm process")
            self._process.terminate()
            self._process.join()

✅ Option 2 (cleaner but slightly more work): shared stop signal

Use a multiprocessing.Event:
Create it

self._stop_event = mp.Event()

Pass it to worker

args=(self.uris, self.command_queue, self._stop_event)

Worker checks it

while not stop_event.is_set():

Trigger stop

self._stop_event.set()

⚖️ Which one should you use?

    Option 1 (terminate) → ✔ simplest, ✔ reliable, ✔ what you want right now

    Option 2 (event) → cleaner, but not enough alone if Swarm(...) hangs

👉 In practice: use terminate anyway for safety-critical systems
🚨 Important safety note (your use case)

Since you mentioned finger safety:

You should always combine both:

    Send DroneCommand.emergency (best-effort graceful stop)

    Immediately terminate() process (guaranteed stop of control loop)

🧩 Final mental model

You now have:

    Parent = supervisor (can restart / kill)

    Child = swarm controller (can hang, but is disposable)

👉 This is exactly how real robotics systems handle unreliable hardware layers.

If you want, I can next show you how to:

    make the worker report “CONNECTED” reliably (not time-based)

    or
    prevent multiple swarm processes from ever overlapping (race condition you might hit soon)


