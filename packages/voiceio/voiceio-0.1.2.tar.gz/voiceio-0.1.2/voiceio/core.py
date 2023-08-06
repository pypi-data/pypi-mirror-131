"""
BSD 3-Clause License

Copyright (c) 2021, Vincent
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from __future__ import unicode_literals

import os
import logging
import yt_dlp

_log = logging.getLogger(__name__)

dir = os.getcwd()
dire = f"{dir}/.voiceio/"

if os.path.isdir(dire) != True:
    os.mkdir(".voiceio/")
else:
    _log.debug("Directory ./voiceio already exists putting files there instead.")


class Process:
    """The voiceio Process Client.

    .. versionadded:: 0.1.0
    """

    def __init__(
        self,
        quality="bestaudio/best",
        chache_dir=".voiceio/",
        duration: bool = True,
        thumbnail: bool = False,
        prefer_ffmpeg: bool = True,
        cookie_file=".voiceio/cookies.txt"
    ):
        yt_dlp_options = {  # https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/__init__.py#L620-L780
            "format": quality,  # the quality to download, defaults to best
            "prefer_ffmpeg": prefer_ffmpeg,  # try to use only FFmpeg, defaults to true.
            "forceduration": duration,  # display the duration of the vid
            "forcethumbnail": thumbnail,  # print thumbnail url
            "chachedir": chache_dir,  # The cachedir, defaults .voiceio/
            "cookiefile": cookie_file,
            "quiet": True, # Makes stuff quiet, Is only true.
        }
        self.voice = yt_dlp.YoutubeDL(yt_dlp_options)

    # TODO; Make it delete after sometime and add possible ratelimit.
    def download( # TODO; get more formats to work them .webm.
        self, url=""
    ) -> callable:  # Currently only allows for the creation of 1 video download per process, need to expand.
        self.voice.download([url])
