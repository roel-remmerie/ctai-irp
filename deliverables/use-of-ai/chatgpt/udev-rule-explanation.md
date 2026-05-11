# cat > /etc/udev/rules.d/99-lps.rules << EOF
SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0664", GROUP="plugdev"
EOF

what does this do

This command creates a udev rule on a Linux system. Let’s break it down.
1. The command itself

cat > /etc/udev/rules.d/99-lps.rules << EOF
...
EOF

    cat > file writes text into a file

    /etc/udev/rules.d/99-lps.rules is where custom udev rules live

    EOF ... EOF is just a way to input multiple lines

So overall: you’re creating a new udev rules file called 99-lps.rules.
2. The rule inside

SUBSYSTEM=="usb", ATTRS{idVendor}=="0483", ATTRS{idProduct}=="df11", MODE="0664", GROUP="plugdev"

This tells the system:

👉 “When a USB device with these IDs is connected, apply these permissions.”
Breakdown:

    SUBSYSTEM=="usb"
    → applies only to USB devices

    ATTRS{idVendor}=="0483"
    → vendor ID = 0483
    (this is STMicroelectronics, commonly used for STM32 devices)

    ATTRS{idProduct}=="df11"
    → product ID = df11
    (typically STM32 in DFU (Device Firmware Upgrade) mode)

3. What permissions it sets

    MODE="0664"
    → device file permissions:

        owner: read/write

        group: read/write

        others: read only

    GROUP="plugdev"
    → assigns the device to the plugdev group

4. What this achieves in practice

Without this rule:

    only root might be able to access the device

With this rule:

    any user in the plugdev group can interact with the device

    useful for:

        flashing firmware

        using tools like dfu-util

        working with STM32 boards without sudo

5. Typical use case

This is commonly added when working with:

    STM32 microcontrollers in DFU mode

    development boards like STM32 Nucleo / Discovery

6. Important follow-up step

After creating the file, you usually need:

sudo udevadm control --reload-rules
sudo udevadm trigger

If you want, I can
help you confirm whether your user is in the plugdev group or
adapt this rule for a different device.

That error just means your system doesn’t have the adduser helper installed (or it’s not in your PATH). It’s common on minimal or non-Debian-based systems.
What to do instead

Use the lower-level command that’s almost always available:

sudo usermod -aG dialout $USER

What this does

    usermod → modifies a user account

    -aG dialout → appends (-a) your user to the dialout group

Important: log out required

Group changes don’t apply immediately. You need to:

logout

or reboot, then log back in.
Quick check

After logging back in:

groups

You should see dialout listed.
Why this matters

As mentioned earlier:

    dialout → access to serial ports (/dev/ttyUSB*, /dev/ttyACM*)

    your udev rule → access to STM32 in DFU mode

If you’re curious, I can also show you how to verify whether your device is hitting the udev rule correctly.

usermod: group 'dialout' does not exist

That means your system simply doesn’t have a dialout group at all, which is normal on some distributions (e.g. Arch, Fedora, Alpine, etc.). The group name is not universal across Linux.
What’s going on

    On Debian/Ubuntu → serial devices use dialout

    On other distros → they often use:

        uucp

        tty

        or something else entirely

So trying to add yourself to dialout fails because it doesn’t exist.
What you should do instead
1. Check which group owns your serial device

Plug in your device, then run:

ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

Example output:

crw-rw---- 1 root uucp 188, 0 ... /dev/ttyUSB0

👉 The important part is the group (uucp in this example)
2. Add yourself to that group

If you see uucp, then:

sudo usermod -aG uucp $USER

If it’s something else (e.g. tty), use that instead.
3. Log out and back in

Same as before—group changes need a new session.
How this relates to your udev rule

Your rule uses:

GROUP="plugdev"

So now you potentially have two groups involved:

    plugdev → for DFU mode (your udev rule)

    uucp (or similar) → for serial communication

Optional: make it consistent

If you want, you can avoid juggling groups by modifying your udev rule to use whatever group your system actually uses (like uucp instead of plugdev).

If you paste the output of your ls -l /dev/... command, I’ll tell you exactly which group you should use.

I'm using arch

That explains it — on Arch Linux there is no dialout group by default.
What Arch uses instead

On Arch, serial devices are typically owned by:

    uucp (most common)

    sometimes tty

What you should do
1. Check your device group

Plug in your board and run:

ls -l /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

You’ll likely see something like:

crw-rw---- 1 root uucp ... /dev/ttyACM0

2. Add yourself to uucp

sudo usermod -aG uucp $USER

3. Log out and back in

This is required for group changes to apply.
About your udev rule

You created:

GROUP="plugdev"

On Arch:

    plugdev usually doesn’t exist either

So you have two options:
Option A (recommended): use uucp

Edit your rule:

GROUP="uucp"

Option B: create plugdev

sudo groupadd plugdev
sudo usermod -aG plugdev $USER

Practical setup for STM32 (typical)

If you're working with STM32:

    DFU mode (flashing) → your udev rule (set to uucp)

    Serial communication → also uucp

👉 So using uucp everywhere keeps things simple.
Reload rules after editing

sudo udevadm control --reload-rules
sudo udevadm trigger

If you want, I can help you verify your STM32 shows up correctly (DFU vs serial mode), since that’s often where things get confusing.


