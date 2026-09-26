import sys
from .game.game import Game
from mazegenerator import MazeGenerator
from .parser.load_config import Config


def main():
    config = Config.from_json_file(sys.argv[1]) 
    game = Game(config)
    game.run()
   # try:
      #  if len(sys.argv) > 1:
     #   else:
     #       raise ValueError("Need a setting file(json) to make life good")
    #except Exception as e:
    #    print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
