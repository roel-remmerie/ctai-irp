I'm following an installation manual https://github.com/bitcraze/lps-tools#running-instruction

USB access right on Linux

On Linux, to be able to flash the node you need to have access right to the node bootloader. This can be achieved by adding a udev rules for the node bootloader.

# cat > /etc/udev/rules.d/99-lps.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0664", GROUP="plugdev"
EOF

Your user also needs to be in the dialout group in order to be able to communicate with the node serial port (you may need to log-out and log-in againt for this to take effect):

sudo adduser $USER dialout

this does not work (I'm using archlinux)

Yeah, those instructions are written with Debian/Ubuntu in mind, so on Arch Linux a couple of details can trip you up. Let’s go through the usual failure points and how to fix them.
1. Check the group names (important on Arch)

On Ubuntu, plugdev is standard. On Arch, it often does not exist by default.
Option A — create the group

sudo groupadd plugdev
sudo usermod -aG plugdev $USER

Option B — easier: use an existing group

Arch commonly uses:

    uucp

    lock

    wheel (not ideal for devices)

So you can modify your rule to:

SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0666", GROUP="uucp"

(0666 is fine for debugging; you can tighten later)
2. Reload udev rules (people often forget this)

After creating the file:

sudo udevadm control --reload-rules
sudo udevadm trigger

Then replug the device.
3. Verify the device is detected correctly

Plug in your device and run:

lsusb

You should see something like:

0483:df11

If not → you're not actually in bootloader mode.
4. Check permissions directly

Find your device:

ls -l /dev/bus/usb/*/*

Or better:

udevadm info -a -n /dev/bus/usb/XXX/YYY

Make sure:

    the rule is applied

    group is correct

    permissions match (rw for your user/group)

5. Serial access (dialout vs Arch)

On Arch, serial devices are usually:

    group: uucp

So instead of:

sudo adduser $USER dialout

Use:

sudo usermod -aG uucp $USER

Then log out and back in (or reboot).
6. Quick sanity test

After all that:

groups

Make sure you see:

    uucp (or plugdev if you used that)

7. If it still fails

Run your flashing command with debug:

sudo dmesg | tail

Look for:

    permission denied

    device not recognized

    wrong mode (normal vs DFU bootloader)

TL;DR fix for Arch

This usually works immediately:

echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0666"' | sudo tee /etc/udev/rules.d/99-lps.rules

sudo udevadm control --reload-rules
sudo udevadm trigger

sudo usermod -aG uucp $USER

Then log out/in and replug the device.

If you still get errors, tell me:

    the exact error message

    output of lsusb

    what command you're running to flash

…and I’ll pinpoint it.

using lpstools (crazyflie loco positioning tools) when configuring a node I get
Error while configuring: [Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied: '/dev/ttyACM0'

That error is very typical on Arch — and it’s almost always just a group/permissions mismatch on /dev/ttyACM0, not the udev rule you added for the bootloader.

Let’s zero in on the actual problem.
🔍 What’s happening

lpstools is trying to access:

/dev/ttyACM0

That’s a serial device, not the USB DFU bootloader.
So your 0483:df11 rule is irrelevant for this error.
✅ Fix (Arch-specific)
1. Check device permissions

Run:

ls -l /dev/ttyACM0

You’ll likely see something like:

crw-rw---- 1 root uucp ... /dev/ttyACM0

👉 The important part is the group: uucp
2. Add yourself to the correct group

On Arch, you need:

sudo usermod -aG uucp $USER

Then:

logout

(or reboot)
3. Verify it worked

After logging back in:

groups

You should see uucp in the list.
4. Quick test

Try:

cat /dev/ttyACM0

If you don’t get permission denied → you're good.
⚠️ Common pitfalls

    ❌ Adding yourself to dialout → does nothing on Arch

    ❌ Not logging out → group change won’t apply

    ❌ Using sudo for everything → hides the real issue

🧪 If it still fails

Check if something else is locking the port:

lsof /dev/ttyACM0

or:

fuser /dev/ttyACM0

💡 Optional: persistent udev rule (cleaner setup)

If you want explicit control:

sudo nano /etc/udev/rules.d/99-ttyacm.rules

Add:

KERNEL=="ttyACM0", MODE="0666"

Then reload:

sudo udevadm control --reload-rules
sudo udevadm trigger

🚀 Bottom line

On Arch, this error is solved by:

sudo usermod -aG uucp $USER

→ logout/login
→ replug device

If you still get the error after that, send me:

    ls -l /dev/ttyACM0

    groups

    exact lpstools command

and I’ll debug it with you step-by-step.


