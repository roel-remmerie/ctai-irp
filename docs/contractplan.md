# CONTRACTPLAN RESEARCHPROJECT REMMERIE ROEL

- **bachelor creative technologies & AI**
- **semester 5**
- **academic year 2025-2026**
- **responsibles**
    - **Nathan Segers**
    - **Paula Acuña Roncancio**
    - **Wouter Gevaert**
    

## 1 INTRODUCTION
### 1.1 IDENTIFICATION

|||
|---|---|
| Date | 27/10/2025 |
| Signed by | **Remmerie Roel** |
| Internal coach Research Project | **Paula Acuña Roncancio** |
| Internal promotor bachelor’s Thesis | not determined |
| External promotor bachelor’s Thesis | not determined |

### 1.2 GOAL
In the Innovation & Research Project and Bachelor’s Thesis modules, you will dive deeper into technical
competences and combine them with some general competences. By the end of this module, you’ll be:
- Able to formulate a question from professional field
- Work structured towards a goal
- Get results by own, technical research
- Take conclusions from your technical research
- Reflect on the conclusions
- Formulate advise
- Present your thesis for a jury of specialists
- Create an attitude for Lifelong Learning

How are we going to start?
1. You start by formulating a research question. It could be from an internship company, from an
inspirational list … A team of teachers will check the level of your question.
2. You perform the practical research at school. The question will be fully researched and
technically implemented during the Innovation & Research Project module in a span of
maximum four weeks.
You’ll create/research your own solution/design/prototype. It could be pushed into a specific
direction by your question.
3. In the bachelor’s Thesis you will reflect individually with experts from the industry (for example
in your internship companies) and with community members that have a great knowledge of
your project.

Below, you will find a few of the different steps. Your goal is to think critically about the different phases
of your research. You will create a plan of approach and think about your process. Try to fill in the form
fields as extensively as possible. You will notice that a great and thorough preparation is a great support
during the creation of your research project and bachelor’s thesis.

## 2 PLAN OF APPROACH
### 2.1 SCOUT THE WORKFIELD AND FILTER

You have received your research question from your teachers, from an internship company, from someone else … but now you need to get some more information about this topic. Most likely, you’ll already have a little bit of knowledge about this. In some cases, it’s a completely new topic. Maybe the question that you have received is still too broad, wide, or generic. You’ll have to dive deeper into your topic to get comfortable.

Read, read and read some sources and fetch information. Keep track of all the sources you have encountered during your research. The more you read into your topic, the clearer your vision will get. As it gets clearer, you can easily define your topic further. Narrowing down is very important:
- What exactly are you going to research?
- Where is your topic located?
- What perspective are you going to research?
- Who are the actors that benefit from this research?

### 2.2 REASEARCH QUESTION AND SUBQUESTIONS

This is your main research question: What question do you wish to research and answer?

**What is the best use of drone swarm AI in Search and rescue operations**

### 2.3 SUB QUESTIONS

Write down a bunch of sub questions to structure your project. It will make sure you can split your
research in chunks with theoretical and practical parts. Some questions will be answered by a literature
study. Other questions will only be answered by practically researching everything.

Try to get a minimum of 5 and a maximum of 10 sub questions. It can be a few smaller and some bigger
questions if needed.

- What is drone swarm AI?
    - What is a drone?
    - What is swarm AI?
- Where and When can a drone operate?
- What are search and rescue operations (SAR Ops)?
- How can a drone detect a target
- How can drone swarm AI be used in SAR Ops?
- What are the risks of using drone swarm AI in SAR Ops?
- What are the advantages of using drone swarm AI in SAR Ops?

### 2.4 THE RESEARCH PROJECT – TECHNICAL RESEARCH
Goal: Your research question will be technically implemented individually (or in a team of two people)
during the practical weeks in January, during a period of maximum four weeks. You’ll create/research
your own solution/design/prototype.

This is the first real practical step as soon as you have formulated your research and sub questions.
You clearly defined what way you want to go to, and now you can formulate all the different steps to get
to that goal. What components are necessary to reach your goal? How are you going to build these
components?

TIP: Write down a mind map (or brainstorm) to structure your approach. Talk this through with
experts/your coach.

What are you going to create as technical research? Make sure your context is well defined, go into
detail where necessary. Use a plan of approach and include images. Don’t forget any important
elements! **Warning: Innovation & Research Project in MCT is always a technical realisation. Only including a literature study is not enough.**
- Which data will you use?
    - greyscale images
    - none for non human target
    - for human target
        - search an rescue datasets SARD
        - human detection in UAV imagery
- What case will you work out?
    - A swarm of Crazyflie drones searches a perimeter for: ...
        1. a single non human target ...
        2. multiple non human targets ...
        3. a single person in distress ...
        4. multiple people in distress ...
    
        as efficiently as possible.
- Which evaluation or comparison criteria will you use?
    - always over multiple trials
    1. a single human piloted Crazyflie vs a swarm AI of Crazyflies for a single target, criteria: average time to target over multiple trials.
    2. a group of mock rescuers vs that same group of mock rescuers assisted by the Crazyflie swarm for multiple targets, criteria: average time to targets over multiple trials.
- What are the minimal requirements of your project / app?
    - a swarm AI of Crazyflies that can find a single non human target more efficiently then a single human pilot.
- How do you make sure your application is relevant?
    - literature study
    - interview with field experts
    - survey (colleagues lifeguards Bredene)

![brainstorm](./images/brainstorm.png)

### 2.5 TECHNICAL RESEARCH: SUCCESS CRITERIA
Now that you have well defined how your project will be made, it is important to define some goals and
success criteria.
- When is your project finished according to your standards? Describe a few of your results that you want to achieve. Use a list.
    - [ ] drones can detect targets
    - [ ] drones can communicate with eachother (swarm AI)
    - [ ] drones explore the perimeter
        - using search algorithms
        - coordinating with swarm AI
    - [ ] drones can execute case [1.](), **A swarm of Crazyflie drones searches a perimeter for a single target faster than a human operated drone**
        - extra use cases [2.]() [3.]() [4.]()

- What will your technical demo or proof-of-concept contain?
    - executing (or showing a video of) the last completed use case 
- When is your project finished?
    - after completing use case [4.]()
- What if you’re done in a few weeks, and you want to do some alternatives?
    - as mentioned previously: extra use cases [2.]() [3.]() [4.]()

### 2.6 HANDING IN YOUR RESEARCH PROJECT

In the end of the Innovation & Research Project, you should hand in all of these required things:
- User manual
    - How can someone use the project that you have developed?
    - What are all the things that one should think of when using this project?
- Installation manual
    - How can someone install this project on their own setup?
    - Where are the pitfalls in the installation?
- Source code
    - During the development of an application, or when writing any code, hand everything in.
- A few more optional things:
    - Technical schema’s
    - Graphical representations of technologies
    - Other illustrations that can be interested for your project
    - Video’s of your demonstration that you created

Talk to your coach about what to hand in in your situation.

### 2.7 Bachelors Thesis

not applicable

### 2.8 SOURCES

#### 2.8.1 Research related

1. S. Sambolek, M. Ivasic-Kos. "SEARCH AND RESCUE IMAGE DATASET FOR PERSON DETECTION - SARD." SEARCH AND RESCUE IMAGE DATASET FOR PERSON DETECTION - SARD | IEEE DataPort. Accessed: Feb. 16, 2026. [Online.] Available: https://ieee-dataport.org/documents/search-and-rescue-image-dataset-person-detection-sard
2. S. Sambolek, M. Ivasic-Kos. "Automatic Person Detection in Search and Rescue Operations Using Deep CNN Detectors." Automatic Person Detection in Search and Rescue Operations Using Deep CNN Detectors | IEEE Journals & Magazine | IEEE Xplore. Accessed: Feb. 16, 2026. [Online.] Available: https://ieeexplore.ieee.org/document/9369386
3. D. P. Simões, H. C. de Oliveira, D. R. Pereira. "Unicamp-UAV: An open dataset for human detection in UAV imagery." Unicamp-UAV: An open dataset for human detection in UAV imagery - ScienceDirect. Accessed: Feb. 16, 2026. [Online.] Available: https://www.sciencedirect.com/science/article/pii/S0924271625004149
4. "Loco Swarm bundle - Crazyflie 2.1+." Loco Swarm bundle - Crazyflie 2.1+ – Bitcraze Store. Accessed: Feb. 16, 2026. [Online.] Available: https://store.bitcraze.io/products/loco-swarm-bundle
5. "AI deck 1.1." AI deck 1.1 | Bitcraze. Accessed: Feb. 16, 2026. [Online.] Available: https://www.bitcraze.io/products/ai-deck/
6. "Flow deck v2." Flow deck v2 | Bitcraze. Accessed: Feb. 16, 2026. [Online.] Available: https://www.bitcraze.io/products/flow-deck-v2/
7. "Mind mapping for everyone." MindMeister | Online Mind Mapping & Brainstorming Software. Accessed: Feb. 17, 2026. [Online.] Available: https://www.mindmeister.com/pages/home-version-1

#### 2.8.2 IEEE related

1. J. Caulfield. "IEEE Website Citation | Guide with Examples." IEEE Website Citation | Guide with Examples. Accessed: Feb. 14, 2026. [Online.] Available: https://www.scribbr.com/ieee/ieee-website-citation/
2. IEEE Author Center. "IEEE Editorial Style Manual." IEEE Editorial Style Manual - IEEE Author Center Journals. Accessed: Feb. 14, 2026. [Online.] Available: https://journals.ieeeauthorcenter.ieee.org/your-role-in-article-production/ieee-editorial-style-manual/
3. IEEE Author Center. "Refrence Guide." IEEE Reference Style Guide for Authors - Google Documenten. Accessed: Feb. 14, 2026. [Online.] Available: https://docs.google.com/document/d/1j1L96U2NagwWI9MEVDNVKt9pXxRzTH7h3krI3Mb6wZE/edit?tab=t.0

#### 2.8.3 Python sources

these were used to create a script that helps with IEEE style sources

```python
from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import pyperclip
import os

REQ_AUTHOR = "Author: "

AUTHOR_EXIT = "none"

def get_authors() -> str:
    authors = ""
    author = input(REQ_AUTHOR)

    while author != AUTHOR_EXIT:
        authors += author        
        author = input(REQ_AUTHOR)
        if author != AUTHOR_EXIT:
            authors += ", "

    if authors != "":
        authors += ". "

    return authors

REQ_URL = "URL: "

def get_url() -> tuple[str, str]:
    url = input(REQ_URL)
    try:
        soup = BeautifulSoup(urlopen(url), features="html.parser")
        website_title = soup.title.get_text()
        return url, website_title
    except Exception:
        print("could not read page")
        website_title = input("Website Title: ")
        return url, website_title

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

ieee_citation = "{authors}\"{page_title}\" {website_title}. Accessed: {month}. {day}, {year}. [Online.] Available: {url}"

def get_citation():
    authors = get_authors()
    page_title = input("Title: ")
    url, website_title = get_url()
    now = datetime.now()

    citation = ieee_citation.format(
        authors=authors,
        page_title=page_title,
        website_title=website_title,
        month = months[now.month],
        day = now.day,
        year = now.year,
        url = url
    )

    return citation

if __name__ == "__main__":
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("IEEE Citation\ninput ^C to quit")
            citation = get_citation()
            print(citation)
            pyperclip.copy(citation)
            input("press Enter to continue ...")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e) 
```

1. N. Mikhailov. "Python.gitignore." gitignore/Python.gitignore at main · github/gitignore · GitHub. Accessed: Feb. 14, 2026. [Online.] Available: https://github.com/github/gitignore/blob/main/Python.gitignore
2. S. Kumar. "Extract title from a webpage using Python." Extract title from a webpage using Python - GeeksforGeeks. Accessed: Feb. 14, 2026. [Online.] Available: https://www.geeksforgeeks.org/python/extract-title-from-a-webpage-using-python/
3. IlanL, K. Kundu. "BeautifulSoup different parsers." python 3.x - BeautifulSoup different parsers - Stackoverflow. Accessed: Feb. 14, 2026. [Online.] Available: https://stackoverflow.com/questions/55880415/beautifulsoup-different-parsers
4. Soviut, R. Duffield, T. Merouane, P. Mortensen. "How can I clear the interpreter console?" python - How can I clear the interpreter console? - Stack Overflow. Accessed: Feb. 14, 2026. [Online.] Available: stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console
5. D. Masquelier, atomizer, D. Lowe, Dreftymac. "How do I copy a string to the clipboard?" python - How do I copy a string to the clipboard? - Stack Overflow. Accessed: Feb. 14, 2026. [Online.] Available: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard
6. Asweigart. "Pyperclip." GitHub - asweigart/pyperclip: Python module for cross-platform clipboard functions.. Accessed: Feb. 14, 2026. [Online.] Available: https://github.com/asweigart/pyperclip

#### 2.8.4 Hounourable mentions

1. Greetje Desnerck
    - assisted with brainstorming

## 3 SIGNATURE

I hereby declare that I will complete my project according to the defined planning like above.

Your (digital) signature.

![signature](./images/signature.png)

Surname and name: Roel Remmerie

Date: 17/02/2026