# Overview

Did you know that centipedes aren't bugs? Well neither is this Chrome feature that gives you access to cookies in plaintext and so much more via remote debugging!

If you can launch any Chromium based browser with `--remote-debugging-port=<some_number>` then you can send websocket requests to it and interact in lots of amazing ways.

This project is a simple Python tool designed as a playground for this attack vector based on the amazin research done by [SpectreOps](https://posts.specterops.io/hands-in-the-cookie-jar-dumping-cookies-with-chromiums-remote-debugger-port-34c4f468844e). The idea is that you run this Python script and send the data over SOCKS to a compromized host.

So far I've implemented the following functionality:

- Get all open tabs/extensions
- Get the cookies for any open page
- Inject arbitrary JS into any page (doesn't work on Edge)
- Get navigation history for a page

Planned future features:

- Screenshot pages
- Hijack pages to make arbitrary requests
- Download arbitrary files

# Usage

Since this is pretty much just a PoC and playground for now I've written this script as a library. It contains a single class (`ChromeInterface`) that has several available functions to execute the functionalities I discover. When executing the script it will just run a quick PoC illustrating these features. I may clean it up into a proper PoC depending on how well it performs in future red teams.

# Contributing

I am always open to issues, feedback, PR's, etc. So please reach out if you have some ideas.
