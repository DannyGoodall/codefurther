.. The convention used for headings here is
   #####
   Parts
   #####
   ========
   Chapters
   ========
   Section
   =======
   Subsection
   ----------
   Subsubsection
   ^^^^^^^^^^^^^
   Paragraph
   """""""""

###############################
Lyrics - Search for song lyrics
###############################

The **Lyrics** module is part of the **codefurther** Python package, and is designed to be used in UK schools to provide
students with access to data that describes the words to popular songs.

**Lyrics** is part of a wider initiative that I'm referring to as **CodeFurther**. The hope is that by providing simple
interfaces to information that is relevant to students, they will be able to relate to the data and imagine more
ways in which they could consume and use it in their code - and hopefully **CodeFurther**.

The data that **Lyrics** accesses is provided by Wikia and should be accessed as as part of its
`Lyrics Wikia site <http://lyrics.wikia.com/Lyrics_Wiki>`_.

.....

========
Features
========

**Lyrics** provides:

* Search for an artist on Lyrics Wikia
* Search for the lyrics of a song by a specific artist
* Search for all of the songs by a specific artist that are present on Lyrics Wikia.

.....

=====
Usage
=====

**Directions** exposes a very simple API to developers. It is accessed by importing the
:class:`~lyrics.Lyrics` class into your module and creating an instance of this class, like so::

   from codefurther.lyrics import Lyrics
   lyrics_machine = Lyrics()

To print out the lyrics to a song, the :py:meth:`Lyrics.song_lyrics` method is used to to find the song, given the
name of the artist and the name of the song.::

    lyrics_list = lyrics_machine.song_lyrics("billy bragg", "days like these")

The lyrics are returned as a :py:class:`list` of :py:class:`str` items, and be printed simply, like so.::

    for count, line in enumerate(lyrics_list):
        print(
            "{}. {}".format(
                count+1,
                line
            )
        )

The :py:class:`~lyrics.Lyrics` instance exposes a number of properties to the programmer. These include:

* :py:attr:`Lyrics.song_lyrics <codefurther.lyrics.Lyrics.song_lyrics>`
* :py:attr:`Lyrics_artist_songs <codefurther.lyrics.Lyrics.artist_songs>`
* :py:attr:`Lyrics_artist_search <codefurther.lyrics.Lyrics.artist_search>`

The example code below shows how you can use these properties. This code, simply returns the lyrics to a song, given
the name of the artist and the name of the song.::

    from codefurther.lyrics import Lyrics

    lyrics_machine = Lyrics()

    lyrics_list = lyrics_machine.song_lyrics("billy bragg", "days like these")

    for count, line in enumerate(lyrics_list):
        print(
            "{}. {}".format(
                count+1,
                line
            )
        )

This results in the following output.::

    1. The party that became so powerful
    2. By sinking foreign boats
    3. Is dreaming up new promises
    4. Because promises win votes
    .
    .
    .
    31. Peace, bread, work, and freedom
    32. Is the best we can achieve
    33. And wearing badges is not enough
    34. In days like these

The following code find all of the songs for a given artist.::

    from codefurther.lyrics import Lyrics

    lyrics_machine = Lyrics()

    song_list = lyrics_machine.artist_songs("billy bragg")

    for count, song in enumerate(song_list):
        print(
            "{}. {}".format(
                count+1,
                song
            )
        )

Resulting in the following output.::

    1. The Milkman of Human Kindness
    2. To Have and to Have Not
    3. Richard
    .
    .
    .
    396. To Have And Have Not
    397. Walk Away Renee
    398. Youngest Son

This code allows the programmer to search for the exact name of an artist.::

    from codefurther.lyrics import Lyrics

    lyrics_machine = Lyrics()

    artist_details = lyrics_machine.artist_search("Billy Bragg")

    print(artist_details)

If an exact match of the artist is not found, then the nearest match is returned.


.....

==========
Lyrics API
==========

.. automodule:: lyrics
	:members:
	:member-order: bysource

