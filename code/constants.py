"""
This module captures constants used across the codebase.
"""

MODELS = ["CM", "CM3x3", "CN", "CN3x3", "CSD", "GLRLM", "GLRLM3x3", "HOG", "LBP", "LBP3x3"]
PROCESSED_VISUAL_DESCRIPTORS_DIR_PATH = "../dataset/visual_descriptors/processed/"
FINAL_PROCESSED_VISUAL_DESCRIPTORS_DIR_PATH = "../dataset/visual_descriptors/final_processed/"
VISUAL_DESCRIPTORS_DIR_PATH_REGEX = "../dataset/visual_descriptors/*.csv"
DEVSET_TOPICS_DIR_PATH = "../dataset/text_descriptors/devset_topics.xml"
VISUAL_DESCRIPTORS_DIR_PATH = "../dataset/visual_descriptors/"
TEXT_DESCRIPTORS_DIR_PATH = "../dataset/text_descriptors/"
DUMPED_OBJECTS_DIR_PATH = "../dumped_objects/"
LOCATION_ID_KEY_ERROR = "Wrong input: Location id not found"
GENERIC_EXCEPTION_MESSAGE = "Exception encountered: "
LOCATION_TEXT = "location"
IMAGE_TEXT = "image"
USER_TEXT = "user"
IMAGE_ID_KEY_ERROR = "Wrong input: Image id not found"
USER_ID_KEY_ERROR = "Wrong input: User id not found"