from prideCats.gender import genderfae, trans, nb, genderfluid
from prideCats.sexualities import lesbian, mlm, bisexual


def run():
    bisexual.generate()
    genderfluid.generate()
    genderfae.generate()
    nb.generate()
    trans.generate()
    lesbian.generate()
    mlm.generate()

if __name__ == "__main__":
    run()