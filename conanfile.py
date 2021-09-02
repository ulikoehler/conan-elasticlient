from conans import ConanFile, CMake, tools


class ElasticlientConan(ConanFile):
    name = "elasticlient"
    version = "0.2"
    license = "MIT"
    author = "seznam (Conan packaging by Uli Köhler <conan@techoverflow.net>)"
    url = "https://github.com/seznam/elasticlient"
    description = "C++ elasticlient library is simple library for simplified work with Elasticsearch in C++. The library is based on C++ Requests: Curl for People"
    topics = ("ElasticSearch",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    requires = (
        "openssl/1.1.1l",
        "cpr/1.6.2",
        "jsoncpp/1.9.4",
        "libcurl/7.78.0",
    )
    build_requires = (
        "gtest/cci.20210126",
    )

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://github.com/seznam/elasticlient.git -b version-0.2")
        self.run("cd elasticlient && git submodule update --init --recursive")

        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("elasticlient/CMakeLists.txt", "project(Elasticlient LANGUAGES CXX)",
                              '''project(Elasticlient LANGUAGES CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')


    def build(self):
        cmake = CMake(self)
        cmake.definitions["USE_SYSTEM_CPR"] = "YES"
        cmake.definitions["USE_SYSTEM_JSONCPP"] = "YES"
        cmake.definitions["USE_SYSTEM_GTEST"] = "YES"
        cmake.definitions["BUILD_ELASTICLIENT_TESTS"] = "NO"
        cmake.definitions["BUILD_ELASTICLIENT_EXAMPLE"] = "NO"
        cmake.configure(source_folder="elasticlient")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="elasticlient/include")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

