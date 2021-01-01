CXX = g++
CXXFLAGS = --std=c++17 -w -O3

SRC_DIR     = ./src
BIN_DIR     = ./bin

$(shell mkdir -p $(BIN_DIR))

SOURCES1 = $(SRC_DIR)/util.cpp 
OBJECTS1 = $(SOURCES1:.cpp=.o)
SOURCES3 = $(SRC_DIR)/sha256.cpp
OBJECTS3 = $(SOURCES3:.cpp=.o)
TARGET1 = repeats
TARGET2 = calc_AU_MFEI
TARGET3 = collapse_hash

default: all

all: repeats calc_AU_MFEI collapse_hash
	
repeats: $(OBJECTS1)
	$(CXX) $(CXXFLAGS) -o $(BIN_DIR)/$(TARGET1) $(OBJECTS1) $(SRC_DIR)/repeats.cpp

calc_AU_MFEI: $(OBJECTS1)
	$(CXX) $(CXXFLAGS) -o $(BIN_DIR)/$(TARGET2) $(OBJECTS1) $(SRC_DIR)/calc_AU_MFEI.cpp

collapse_hash: $(OBJECTS3) $(OBJECTS1)
	$(CXX) $(CXXFLAGS) -o $(BIN_DIR)/$(TARGET3) $(OBJECTS1) $(OBJECTS3) $(SRC_DIR)/collapse_hash.cpp

clean: 
	rm -rf $(OBJECTS1) $(OBJECTS3) $(BIN_DIR)/$(TARGET1) $(BIN_DIR)/$(TARGET2) $(BIN_DIR)/$(TARGET3) $(BIN_DIR)
