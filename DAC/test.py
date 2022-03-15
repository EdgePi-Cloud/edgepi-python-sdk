from DAC import EdgePi_DAC


def main():
    dac = EdgePi_DAC()
    dac.write_and_update(0, 3000)

if __name__ == '__main__':
    main()