#!/bin/bash
#
# Mirrors website using wget
#
# Adapted from https://gist.github.com/mullnerz/9fff80593d6b442d5c1b
# ?permalink_comment_id=3619234#gistcomment-3619234

echo -n "Website to mirror: "
read website

wget \
--convert-link \
--mirror \
--page-requisites \
--continue \
--convert-links \
--html-extension \
--adjust-extension \
--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36." \
--referer="$website" \
--execute robots=off \
$website
