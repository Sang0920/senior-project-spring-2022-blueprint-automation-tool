import os
import time

from blueprint_automation_tool.builder import PlaceBuilder
from blueprint_automation_tool.place_parser import PlaceParser
from blueprint_automation_tool.window import WindowHandler


def benchmark_builder():
    """
    Benchmark the builder.
    """

    _here = os.path.dirname(os.path.abspath(__file__))
    ref_file = os.path.join(_here, "benchmark_files", "reference.kml")
    build_files = [
        os.path.join(_here, "benchmark_files", "reference.kml"),
        os.path.join(_here, "benchmark_files", "2_points.kml"),
        os.path.join(_here, "benchmark_files", "4_points.kml"),
        os.path.join(_here, "benchmark_files", "8_points.kml"),
        os.path.join(_here, "benchmark_files", "16_points.kml"),
        os.path.join(_here, "benchmark_files", "32_points.kml"),
    ]
    print(ref_file)

    times = {}

    builder = PlaceBuilder()
    parser = PlaceParser()
    window_handler = WindowHandler()

    current_window = window_handler.get_current_window()
    ref_place = parser.parse_place(ref_file)[0]

    for file in build_files:
        for scale in [0.5, 1.0, 2.0]:
            time.sleep(1)

            start = time.time()
            builder.build_place(ref_place, [file], 0, "concrete", scale)
            stop = time.time()
            times[f"{file}_{scale}"] = stop - start

            window_handler.set_current_window(current_window)
    with open("benchmarks.csv", "w") as f:
        f.write("Benchmark, Time (Seconds)\n")
        for benchmark in times:
            f.write(f"{benchmark},{times[benchmark]}\n")


if __name__ == "__main__":
    benchmark_builder()
