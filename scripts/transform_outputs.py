from synthetic_politics.transform import transformAll


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--speechOut", required=True)
    parser.add_argument("--chunksOut", required=True)
    args = parser.parse_args()

    n_speeches, n_chunks = transformAll(args.raw, args.speechOut, args.chunksOut)
    print(f"Saved {n_speeches} speeches and {n_chunks} chunks")
