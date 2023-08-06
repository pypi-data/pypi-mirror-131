from .cli import CLI
import fire
def main():
    fire.Fire(CLI().fire)

if __name__ == '__main__':
    main()