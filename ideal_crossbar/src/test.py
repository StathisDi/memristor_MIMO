import argparse


def read_arg():
    parser = argparse.ArgumentParser(
        description="Python simulation for memristor crossbar (experiments with variations)"
    )
    parser.add_argument("rows", help="Initial number of rows.")
    parser.add_argument("cols", help="Upper limit number of rows.")
    parser.add_argument("rep", help="repetition.")
    parser.add_argument("sigma_absolute", help="Set values for sigma absolute")
    parser.add_argument("sigma_relative", help="Set values for sigma relative")

    args = parser.parse_args()
    return args


def main():
    args = read_arg()
    # verification_tb()
    Ron = 1.0e3  # in kOhm
    Roff = 1.0e6  # in kOhm
    sigma_relative = 0.02438171519582677
    sigma_absolute = 0.005490197724238527
    sigma_relative = 0.1032073708277878
    sigma_absolute = 0.005783083695110348
    rows = int(args.rows)
    cols = int(args.cols)
    rep = int(args.rep)
    sigma_absolute = float(args.sigma_absolute)
    sigma_relative = float(args.sigma_relative)
    print("SA ", sigma_absolute, " SR ", sigma_relative, " RE ", rep, " R ", rows, " C ", cols)


if __name__ == "__main__":
    main()
