from data_extract_load.sources import make_pipeline, swedavia_source, wikipedia_source


def run_swedavia() -> None:
    load_info = make_pipeline("swedavia_flights").run(swedavia_source())
    print(load_info)


def run_wikipedia() -> None:
    load_info = make_pipeline("wikipedia_reference").run(wikipedia_source())
    print(load_info)


if __name__ == "__main__":
    #run_wikipedia()   #loaded once and now static, i comment out to make it static and rerun only when needed
    run_swedavia()
