# Youtube comment clusterisation

Pet project

## Usage

At the moment this package allows you to parse a number of comments from YouTube according to the list of video IDs, without using the Youtube API

## Parsing

1. Clone this repository to your machine.
2. Make sure Python 3.8 and [Poetry](https://python-poetry.org/docs/) are installed on your machine (I use Poetry 1.1.13).
3. Install the project dependencies (*run this and following commands in a terminal, from the root of a cloned repository*):

```
poetry install --no-dev
```

4. Run parsing with the following command:

```
poetry run download -p <path to csv with IDs of Youtube videos> -o <output filename data/comments.json default>
```

VideoId - part at the end of the link, for example, the video id under the link `https://www.youtube.com/watch?v=dQw4w9WgXcQ` will be `dQw4w9WgXcQ`

You can configure additional options (such as comment per video limit) in the CLI. To get a full list of them, use help:

```
poetry run train --help
```

Structure of received comments:

```
{
    "cid": "UgwnFmeq9gHhEtu7aId4AaABAg",
    "text": "You're welcome 😊",
    "time": "1 месяц назад",
    "votes": "322",
    "time_parsed": 1650090317.98419
}
```
