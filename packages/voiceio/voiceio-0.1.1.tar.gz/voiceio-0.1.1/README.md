# VoiceIO
Voice package for Pycord adding extra features.

[![Pycord](https://discordapp.com/api/guilds/881207955029110855/embed.png?style=banner2)](https://discord.gg/pycord)

# Example
Down bellow is an example of what you can currently do.

```py
import voiceio

process = voiceio.Process()

@process.download(url="https://www.youtube.com/watch?v=dP15zlyra3c") # Downloads the given link. 
# Full List of supported WebSites: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md
async def y():
    pass
```
