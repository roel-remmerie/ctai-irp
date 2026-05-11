<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# class Result():

    def __init__(self):
        self.success = False
        self.error_message: str = ""
        self.data : t = 
        self.t =
    how can I make abstract in python

In Python, you make a class “abstract” by using the `abc` module and defining at least one method as abstract. Abstract classes are meant to be base classes that you inherit from, not instantiate directly.[^1_1][^1_3][^1_7]

### Minimal abstract class

Here’s how to make an abstract class with an abstract method:

```python
from abc import ABC, abstractmethod

class AbstractResult(ABC):
    def __init__(self):
        self.success = False
        self.error_message: str = ""

    @abstractmethod
    def process(self) -> None:
        """Subclasses must implement this method."""
        pass
```

- `ABC` is the base class that makes `AbstractResult` abstract.[^1_5][^1_1]
- `@abstractmethod` marks `process` as required; subclasses must override it, or you’ll get a `TypeError` when trying to instantiate them.[^1_3][^1_7]


### Concrete subclass example

```python
class ConcreteResult(AbstractResult):
    def __init__(self):
        super().__init__()
        self.data = None

    def process(self) -> None:
        if self.success:
            print("Processing data...")
        else:
            print("Error:", self.error_message)
```

Now you can create `ConcreteResult()` but not `AbstractResult()` directly.[^1_1][^1_5]

If you tell me what you want `data` to be (`t`), I can also integrate that typing into the abstract base.
<span style="display:none">[^1_10][^1_2][^1_4][^1_6][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://www.datacamp.com/tutorial/python-abstract-classes

[^1_2]: https://stackoverflow.com/questions/55893085/making-a-class-abstract-in-python

[^1_3]: https://stackoverflow.com/questions/13646245/is-it-possible-to-make-abstract-classes-in-python

[^1_4]: https://discuss.python.org/t/enforcing-init-signature-when-implementing-it-as-an-abstractmethod/75690

[^1_5]: https://www.scaler.com/topics/abstract-class-in-python/

[^1_6]: https://www.reddit.com/r/learnpython/comments/1bm9e65/abstract_class_how_to_create_it_properly/

[^1_7]: https://docs.python.org/3/library/abc.html

[^1_8]: https://towardsdatascience.com/how-to-use-abstract-classes-in-python-d4d2ddc02e90/

[^1_9]: https://www.youtube.com/watch?v=97V7ICVeTJc

[^1_10]: https://discuss.python.org/t/python-class-init-and-self/66662


---

# I meant instead of abstract you can set the tap at class initialization

You’re asking how to avoid an *abstract* base class and instead set the “type” (or `T`) of `data` at class initialization, using regular Python + `typing`. There are two common patterns that fit what you mean.

***

### 1. Non‑generic class with `data` set at `__init__`

If you don’t care about strict generic‑style type‑checking, just let `data` be “whatever you pass in”:

```python
class Result:
    def __init__(self, data=None):
        self.success = False
        self.error_message: str = ""
        self.data = data
```

Usage:

```python
r1 = Result(123)            # data is int
r2 = Result("hello")        # data is str
```

Type checkers will usually infer `Any` for `self.data` unless you add a type hint.

***

### 2. Generic class where `T` is fixed by the constructor

If you want type‑safe generics (e.g., `Result[int]` or `Result[str]`), use `TypeVar` and `Generic`:

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Result(Generic[T]):
    def __init__(self, data: T):
        self.success: bool = False
        self.error_message: str = ""
        self.data: T = data
```

Usage:

```python
r_int = Result(42)          # inferred as Result[int]
r_str = Result("ok")        # inferred as Result[str]
```

Here the “tap” or choice of `T` is set at initialization, not by inheritance, and type checkers know what `data` is.[^2_1][^2_2][^2_3]

If you paste your exact `Result` code (with `t` and `self.t`), I can rewrite it using one of these patterns so the “type is set at class initialization” instead of needing an abstract base.
<span style="display:none">[^2_10][^2_4][^2_5][^2_6][^2_7][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://typing.python.org/en/latest/spec/generics.html

[^2_2]: https://typing.python.org/en/latest/reference/generics.html

[^2_3]: https://mypy.readthedocs.io/en/latest/generics.html

[^2_4]: https://stackoverflow.com/questions/70349916/using-class-variable-for-type-hinting-in-init

[^2_5]: https://stackoverflow.com/questions/64858261/how-to-use-default-values-in-init-in-a-generic-class

[^2_6]: https://realpython.com/python-class-constructor/

[^2_7]: http://www.w3schools.com/PYTHON/python_class_init.asp

[^2_8]: https://github.com/python/typing/discussions/1084

[^2_9]: https://typing.python.org/en/latest/spec/class-compat.html

[^2_10]: https://docs.python.org/3/library/types.html


---

# does this work?

value: bool = bool(uris)

Yes, this line:

```python
value: bool = bool(uris)
```

is valid Python and will work as long as `uris` is defined and can be converted to a boolean.[^3_6]

### What it does

- `bool(uris)` converts `uris` to `True` or `False` using Python’s truthiness rules:
    - Empty sequences/collections (like `[]`, `{}`, `""`) → `False`.
    - Non‑empty sequences/collections → `True`.
    - `None` → `False`; most non‑zero numbers and non‑empty objects → `True`.[^3_6]
- The annotation `value: bool` just tells type checkers that the variable is intended to be a `bool`; it doesn’t change runtime behavior.[^3_6]


### Example

```python
uris = ["http://example.com"]
value: bool = bool(uris)
print(value)  # True

uris = []
value: bool = bool(uris)
print(value)  # False
```

So your snippet is fine; just make sure `uris` exists in scope and is something that can be converted to a boolean value.
<span style="display:none">[^3_1][^3_10][^3_2][^3_3][^3_4][^3_5][^3_7][^3_8][^3_9]</span>

<div align="center">⁂</div>

[^3_1]: https://api.pygobject.gnome.org/Gst-1.0/structure-Query.html

[^3_2]: http://docs.python-soco.com/en/v0.30.9/_modules/soco/core.html

[^3_3]: https://gitlab-forge.din.developpement-durable.gouv.fr/share/dis-public/gpa/python-apt/-/blob/2.8.y/aptsources/sourceslist.py

[^3_4]: https://clouddocs.f5.com/sdk/f5-sdk-python/apidocs/source/f5sdk.utils.http_utils.html

[^3_5]: https://falcon.readthedocs.io/en/latest/api/routing.html

[^3_6]: https://pydantic.dev/docs/validation/1.10/usage/types/

[^3_7]: https://xrpl.org/docs/tutorials/sample-apps/credential-issuing-service-in-python

[^3_8]: https://pythonhosted.org/sphinx-jsondomain/usage.html

[^3_9]: https://mintlify.com/microsoft/markitdown/guides/python-api

[^3_10]: https://docs.wandb.ai/weave/reference/python-sdk/trace/weave_client


---

# how do i avoid redrawing the background in the while loop of pygame

You can’t *fully* avoid redrawing the background in Pygame’s main loop and still have smooth animation, but you can **minimize overdraw** or make the background “static” so it doesn’t slow you down.

### 1. Draw the background once, then only blit moving objects

If your background never changes, draw it once outside the loop and then only redraw moving parts:

```python
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Draw background once
screen.fill((0, 0, 0))  # or blit a background image
pygame.display.flip()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear only the area where sprites move (or clear whole screen)
    screen.fill((0, 0, 0))

    # Move and blit your sprites here
    # screen.blit(player_img, player_rect)
    # screen.blit(enemy_img, enemy_rect)

    pygame.display.flip()
```

Here you’re still “redrawing” the filling, but you control when and how much.

### 2. Dirty‑rect rendering (only redraw changed areas)

If you want to avoid redrawing the *entire* screen, track “dirty” rectangles and pass them to `pygame.display.update()`:

```python
dirty_rects = []

# each frame:
screen.blit(player_img, player_rect)
dirty_rects.append(player_rect)
dirty_rects.append(old_player_rect)  # where the player was before

pygame.display.update(dirty_rects)
dirty_rects.clear()
```

This tells Pygame to refresh only the changed regions, not the whole background.[^4_1][^4_2]

### 3. Use `pygame.sprite` helpers (`DirtySprite` / `LayeredDirty`)

For more advanced control, use Pygame’s `DirtySprite` and `LayeredDirty`:

```python
from pygame.sprite import LayeredDirty, DirtySprite

group = LayeredDirty()
# ... add DirtySprite objects

while True:
    rects = group.draw(screen)
    pygame.display.update(rects)
```

`rects` is the list of changed areas, so again only those parts are redrawn.[^4_3][^4_1]

### 4. When it’s fine to redraw the whole background

For most games, rerendering the full background every frame is actually acceptable and simpler:

```python
while True:
    screen.blit(bg, (0, 0))   # redraw background every frame
    # blit sprites here
    pygame.display.flip()
```

Performance only becomes a problem if the background is huge, complex, or you’re on very low‑end hardware.[^4_4][^4_2]

If you paste your current loop code, I can rewrite it to either:

- keep the background static and only redraw moving objects, or
- use dirty‑rect logic so only changed areas are updated.
<span style="display:none">[^4_10][^4_5][^4_6][^4_7][^4_8][^4_9]</span>

<div align="center">⁂</div>

[^4_1]: https://stackoverflow.com/questions/52353439/what-is-the-best-way-to-redraw-a-pygame-window

[^4_2]: https://www.pygame.org/docs/tut/newbieguide.html?highlight=pos

[^4_3]: https://www.reddit.com/r/pygame/comments/4qcrul/rerendering_all_text_images_each_frame/

[^4_4]: https://www.pygame.org/docs/tut/tom_games2.html

[^4_5]: https://www.techwithtim.net/tutorials/game-development-with-python/side-scroller-pygame/background

[^4_6]: https://stackoverflow.com/questions/72578230/how-do-you-rotate-an-image-in-pygame-without-constantly-redrawing-the-background

[^4_7]: https://stackoverflow.com/questions/16122990/avoid-to-reload-a-background-at-every-frame-in-pygames

[^4_8]: https://www.youtube.com/watch?v=ZlgNM1pALrI

[^4_9]: https://www.reddit.com/r/pygame/comments/7h354s/only_draw_background_once/

[^4_10]: https://runebook.dev/en/articles/pygame/ref/display/pygame.display.update


---

# class SwarmService():

    def __init__(self):
        self.uris: list[str] = []
        self.process = {
            SCAN: self.scan_drones,
            SEND: self.send_drones,
            RECALL: self.recall_drones
        }
    
    
    def scan_drones(self):
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        self.uris = [f"{aa[0]}/{RADIO_ADDRESS}" for aa in available if aa[0] != USB_DEFAULT_ADDRESS]
        return self.uris
    
    
    def send_drones(self):
        pass
    
    
    def recall_drones(self):
        pass
    how do i use the process dictionary to call events

You use the `process` dictionary by indexing it with a key (like `SCAN`, `SEND`, etc.) to get the corresponding method, then calling it with `()`.

Assuming `SCAN`, `SEND`, `RECALL` are constants (e.g., strings or enums) defined somewhere in your module:

```python
# Example constants at module level
SCAN = "scan"
SEND = "send"
RECALL = "recall"
```

Then in `SwarmService` you can do:

```python
class SwarmService():
    def __init__(self):
        self.uris: list[str] = []
        self.process = {
            SCAN: self.scan_drones,
            SEND: self.send_drones,
            RECALL: self.recall_drones,
        }

    def scan_drones(self):
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        self.uris = [f"{aa[^5_0]}/{RADIO_ADDRESS}" for aa in available if aa[^5_0] != USB_DEFAULT_ADDRESS]
        return self.uris

    def send_drones(self):
        pass

    def recall_drones(self):
        pass

    def run_event(self, event_type):
        """Run the handler corresponding to event_type."""
        handler = self.process.get(event_type)
        if handler is not None:
            return handler()      # call the bound method
        else:
            raise ValueError(f"Unknown event type: {event_type}")
```


### Usage example

```python
swarm = SwarmService()

# Call the correct method via the dictionary
uris = swarm.run_event(SCAN)          # calls scan_drones()
swarm.run_event(SEND)                 # calls send_drones()
swarm.run_event(RECALL)               # calls recall_drones()
```

Key points:

- Store the methods without `()`: `self.scan_drones`, not `self.scan_drones()`.[^5_1][^5_2][^5_3]
- Retrieve and call with `handler()` inside your event dispatcher.[^5_2][^5_3]

If you tell me how `SCAN`/`SEND`/`RECALL` are defined (strings, `int`, `Enum`, etc.), I can adjust the example to match your setup.
<span style="display:none">[^5_10][^5_4][^5_5][^5_6][^5_7][^5_8][^5_9]</span>

<div align="center">⁂</div>

[^5_1]: https://ruepprich.com/python-use-a-dictionary-to-control-function-calling/

[^5_2]: https://www.geeksforgeeks.org/python/python-store-function-as-dictionary-value/

[^5_3]: https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute

[^5_4]: https://www.geeksforgeeks.org/python/python-dictionary-methods/

[^5_5]: https://www.tensorflow.org/api_docs/python/tf/keras/metrics/Recall

[^5_6]: https://www.w3schools.com/python/python_ref_dictionary.asp

[^5_7]: https://towardsdatascience.com/python-constants-everything-you-need-to-know-c3fc66609821/

[^5_8]: https://www.facebook.com/groups/118355661537061/posts/5602229103149662/

[^5_9]: https://stackoverflow.com/questions/20227051/how-to-document-a-module-constant-in-python

[^5_10]: https://www.reddit.com/r/learnpython/comments/zk8kld/can_you_use_a_dictionary_to_pick_a_function_to_run/


---

# sorry I meant execute the methods

To **execute the methods** stored in your `process` dictionary, you just:

1. Look up the method by key (e.g., `SCAN`).
2. Call it with `()`.

### Full example

Assume you have constants like:

```python
SCAN = "scan"
SEND = "send"
RECALL = "recall"
```

Then in your class:

```python
class SwarmService():
    def __init__(self):
        self.uris: list[str] = []
        self.process = {
            SCAN: self.scan_drones,
            SEND: self.send_drones,
            RECALL: self.recall_drones
        }

    def scan_drones(self):
        cflib.crtp.init_drivers()
        available = cflib.crtp.scan_interfaces()
        self.uris = [f"{aa[^6_0]}/{RADIO_ADDRESS}" for aa in available if aa[^6_0] != USB_DEFAULT_ADDRESS]
        return self.uris

    def send_drones(self):
        print("Sending drones...")

    def recall_drones(self):
        print("Recalling drones...")

    def run_event(self, event_type):
        """Execute the method associated with event_type."""
        handler = self.process.get(event_type)
        if handler is not None:
            return handler()      # actually call the method
        else:
            raise ValueError(f"Unknown event type: {event_type}")
```


### How to use it

```python
swarm = SwarmService()

# Execute scan_drones()
uris = swarm.run_event(SCAN)

# Execute send_drones()
swarm.run_event(SEND)

# Execute recall_drones()
swarm.run_event(RECALL)
```

The key idea:

- Store just the method name without `()`: `self.scan_drones`,
- Retrieve and call with `()`: `self.process[SCAN]()`.[^6_1][^6_2]
<span style="display:none">[^6_10][^6_3][^6_4][^6_5][^6_6][^6_7][^6_8][^6_9]</span>

<div align="center">⁂</div>

[^6_1]: https://stackoverflow.com/questions/9168340/using-a-dictionary-to-select-function-to-execute

[^6_2]: https://www.reddit.com/r/learnpython/comments/zk8kld/can_you_use_a_dictionary_to_pick_a_function_to_run/

[^6_3]: https://www.w3schools.com/python/python_ref_dictionary.asp

[^6_4]: https://www.geeksforgeeks.org/python/python-dictionary-methods/

[^6_5]: https://ipcisco.com/lesson/python-dictionary-methods/

[^6_6]: https://www.youtube.com/watch?v=u0yr9B3nH8c

[^6_7]: https://favtutor.com/blogs/python-dictionary

[^6_8]: https://www.datacamp.com/tutorial/python-dictionary-methods

[^6_9]: https://www.youtube.com/watch?v=JwF1E0AVFJY

[^6_10]: https://dev.to/usooldatascience/a-quick-guide-to-python-dictionary-methods-with-examples-2gfb


---

# I need a single word for a variable that indicates that there are no available drone devices

A good single word is **unavailable**.

If you want a variable name, these are clean options:

- `unavailable`
- `empty`
- `none_available`
- `no_drones`

For a boolean flag, the clearest one is:

- `available = False`

For your case, I’d use `unavailable` if you want a state, or `available` if you want a true/false flag.
<span style="display:none">[^7_1][^7_2][^7_3][^7_4][^7_5][^7_6][^7_7]</span>

<div align="center">⁂</div>

[^7_1]: https://www.dslrpros.com/blogs/drone-trends/drone-vocabulary-glossary-terminology

[^7_2]: https://thesaurus.yourdictionary.com/drone

[^7_3]: https://en.wikipedia.org/wiki/Unmanned_aerial_vehicle

[^7_4]: https://www.onelook.com/thesaurus?s=cluster%3A3877

[^7_5]: https://www.thesaurus.com/browse/drone

[^7_6]: https://www.reddit.com/r/djiphantom/comments/3cfsid/why_dont_you_like_the_term_drone_to_be_used_when/

[^7_7]: https://reversedictionary.org/wordsfor/drones

