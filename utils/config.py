import configparser
import glob

configFolder = ('../' if __name__ == '__main__' else './') + 'conf'
configFiles = glob.glob(f"{configFolder}/*.ini")
config = configparser.ConfigParser()
config.read(configFiles)

