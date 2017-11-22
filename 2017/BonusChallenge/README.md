Advent Of Code Bonus Challenge 2017

 * http://adventofcode.com/
 * https://www.reddit.com/r/adventofcode/comments/72aizu/bonus_challenge/
 * https://gist.github.com/topaz/15518587415ccd0468767aed4192bfd3

The puzzle input (`bc-input.txt`) runs through the assembunny interpreter ([Advent Of Code 2016 day 25](http://adventofcode.com/2016/day/25))
and generates a screen program
([Advent Of Code 2016 day 8](http://adventofcode.com/2016/day/8)).
The screen program runs
through the screen interpreter to generate the output:

```
      ##        ##        ##    #    #  ####
     #  #      #  #      #  #  # #  ##     #
     #  #  ##  #            #  # #   #    #
     #### #  # #           #   # #   #    #
     #  # #  # #  #       #    # #   #   #
     #  #  ##   ##       ####   #   ###  #
```

To run:

```shell
./assembunny.py bc-input.txt > screen-input.txt
./screen.py screen-input.txt
```
