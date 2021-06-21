py_library(
    name = "rules-n-todoslib",
    srcs = [
        "utils.py",
    ],
)

py_binary(
    name = "start",
    srcs = [
        "rules-n-todos.py",
    ],
    deps = [
        ":rules-n-todoslib",
    ],
    main = "rules-n-todos.py",
)

py_test(
    name = "test",
    srcs = [
        "utils_tests.py",
    ],
    deps = [
        ":rules-n-todoslib",
    ],
    main = "utils_tests.py",
)