<h1>pod2gen - Generate RSS feeds for podcasts with ease using Python</h1>
<b>Compatible with <a href="https://podcastindex.org/namespace/1.0">podcasting 2.0 RSS namespace extensions</a></b>. This module is an enhanced and maintained fork of [python-podgen](https://github.com/tobinus/python-podgen).

<p align="center">
  <img src="doc/_static/mascot.png" width="600"/>
</p>

> “In the truest sense, freedom cannot be bestowed; it must be achieved.” - Franklin D. Roosevelt

[![Build Status](https://gitlab.com/caproni-podcast-publishing/pod2gen/badges/master/pipeline.svg)](https://gitlab.com/caproni-podcast-publishing/pod2gen/badges/master/pipeline.svg)
[![Test Coverage](https://gitlab.com/caproni-podcast-publishing/pod2gen/badges/master/coverage.svg)](https://gitlab.com/caproni-podcast-publishing/pod2gen/badges/master/coverage.svg)
[![Pypi version](https://shields.io/pypi/v/pod2gen)](https://shields.io/pypi/v/pod2gen)
[![Python version](https://shields.io/pypi/pyversions/pod2gen)](https://shields.io/pypi/pyversions/pod2gen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/pod2gen/badge/?version=latest)](http://pod2gen.readthedocs.io/en/latest/?badge=latest)
[![License](https://shields.io/pypi/l/pod2gen)](https://shields.io/pypi/l/pod2gen)

This module can be used to generate podcast feeds in RSS format and is compatible with Python 3.6+.

🚀 Installation
--------------------------
`pip install pod2gen`


‼️ Important Links
--------------------------
| Repository                                            | Documentation              | Python Package Index                  |
| ----------------------------------------------------- | -------------------------- | ------------------------------------- |
| https://gitlab.com/caproni-podcast-publishing/pod2gen | https://pod2gen.caproni.fm | https://pypi.python.org/pypi/pod2gen/ |

See the documentation link above for guides on how to use this module.

🎙️ RSS Namespace Extension for Podcasting
--------------------------

pod2gen is a fork of [python-podgen](https://github.com/tobinus/python-podgen) that adds support for 
[RSS Namespace Extension for Podcasting](https://podcastindex.org/namespace/1.0),
a wholistic RSS namespace for podcasting that is meant to synthesize the fragmented 
world of podcast namespaces. 

All the tags described in the document 
[RSS Namespace Extension for Podcasting](https://podcastindex.org/namespace/1.0) 
are implemented in pod2gen.


Some cool tags you might be interested in:

```python
from pod2gen import Episode, Funding, Podcast, Soundbite, Transcript

podcast = Podcast()
my_episode = Episode()

# Let people know how they can fund your podcast!

f = Funding("Please support me!", "https://examples.com/donation_link.html")
podcast.add_funding(f)

# Make transcripts accesible

t = Transcript("https://examples.com/transcript_sample.txt", "text/html", language="es", is_caption=False)
my_episode.add_transcript(t)

# Create short episode soundbites

s = Soundbite(1234.5, 42.25, text="Why the Podcast Namespace Matters")
my_episode.add_soundbite(s)
```

And there is a lot more! [Checkout our docs for more details](https://pod2gen.caproni.fm)

🐛 Known bugs and limitations
--------------------------

* The updates to Apple's podcasting guidelines since 2016 have not been
  implemented. This includes the ability to mark episodes
  with episode and season number, and the ability to mark the podcast as
  "serial". It is a goal to implement those changes in a future release.
* We do not follow the RSS recommendation to encode &amp;, &lt; and &gt; using
  hexadecimal character reference (eg. `&#x3C;`), simply because lxml provides
  no documentation on how to do that when using the text property.

⚡️ Why pod2gen? Our Manifesto
--------------------------  
Podcasting is a stronghold for independent content creators. Even as the web is becoming beholden to big proprietary platforms podcasting remains decentralized. Listening to podcasts continues to be one of the most popular uses of RSS. Thanks in part to RSS both podcast listeners and producers enjoy a great deal of freedom and control. 

However, there are companies out there that seem to want to take over podcasting in order to create the YouTube of the spoken word. In order to help stop that from happening the [Podcast Index](https://podcastindex.org/) was created with the mission to "preserve, protect and extend the open,independent podcasting ecosystem". 

We want to support the efforts of the Podcast Index by developing software such as this module. pod2gen makes it easy to build podcasting 2.0 feeds as specified by the Podcast Index community. Podcasting 2.0 enhances podcasting so that it provides more value to listeners and so that it offers content creators more ways to monetize and grow without having to give away control and freedom.

🎪 Contributors
--------------------------
Major credit to [Thorben Dahl](https://github.com/tobinus), author of [python-podgen](https://github.com/tobinus/python-podgen). python-podgen served as the basis for pod2gen.

pod2gen was created by [caproni](https://caproni.fm/en/), a podcast publishing platform. **At caproni we aim to become the first podcast host to fully support Podcasting 2.0!**

We will slowly open source more parts of our platform as reusable independent modules in order to help others adopt Podcasting 2.0. [Sign up for news about new module releases and updates about our Podcasting 2.0 support!](https://caproni.fm/en/podcasting-2)

📝 License
--------------------------
pod2gen is licensed under the terms of both, the FreeBSD license and the LGPLv3+.
Choose the one which is more convenient for you. For more details have a look
at license.bsd and license.lgpl.