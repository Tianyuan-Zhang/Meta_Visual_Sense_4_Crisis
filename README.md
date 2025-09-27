# Social Media Image Interpretation for R-IOSUITE CrizInnov

This depot is part of the CrizInnov project. This work aims at establishing an image processing workflow to facilitate crisis management.

More specifically, the image processing workflow consists of using images posted at social media platforms (mainly Twitter) as the data source, performing deep learning-based classification as the main image interpretation process, extracting crisis-related information from raw images and converting them into concepts and attributes according to a crisis-oriented meta-model, thus updating the situation model and enhancing the situational awareness under crisis context.

The workflow is designed to be integrated into R-IOSUITE.

## 1. Setup

- Install [R-IOSUITE](https://r-iosuite.atlassian.net/wiki/spaces/RIOSUITE/overview?mode=global)
  - Both the `R-IOSUITE Standalone` and the `CrizInnov Connector` should be installed at first.
- Connect R-IOSUITE with Neo4j
  - Follow the guidance: [How to connect R-IOSUITE with Neo4j](https://r-iosuite.atlassian.net/wiki/spaces/RIOSUITE/pages/495420/How+to+connect+Riosuite+with+Neo4j)
- Create Python environment via conda
  - `conda env create -f environment.yml`

## 2. Run the demo

- Start Neo4j Server
  - Follow the guidance: [How to connect R-IOSUITE with Neo4j](https://r-iosuite.atlassian.net/wiki/spaces/RIOSUITE/pages/495420/How+to+connect+Riosuite+with+Neo4j)
- Start R-IOSUITE
  - Both the `R-IOSUITE Standalone` and the `CrizInnov Connector`.
- Load the `Aude Flooding` use case in R-IOSUITE
- Activate the python environment created previously
  - `conda activate xxx`
- Run the Jupyter Notebook built for the 2018 Aude Flood demo
  - The Jupyter Notebook file is located at `./demo/`

## 3. Description

- `./resources/`
  - `./resources/neural-networks/` contains four pre-trained neural networks to perform image classification.
    - These networks are based on [EfficientNet](https://arxiv.org/abs/1905.11946) and implemented with [EfficientNet-PyTorch](https://github.com/lukemelas/EfficientNet-PyTorch)
    - These networks are fine-tuned using the [MEDIC dataset](https://crisisnlp.qcri.org/medic/).
      - More information about the different tasks and corresponding labels can be found in this [link](https://crisisnlp.qcri.org/medic/).
    - The `informative` network will classify images into 2 classes:
      - 0: informative
      - 1: not_informative
    - The `disaster_types` network will classify images into 7 classes:
      - 0: earthquake
      - 1: fire
      - 2: flood
      - 3: hurricane
      - 4: landslide
      - 5: not_disaster
      - 6: other_disaster
    - The `humanitarian` network will classify images into 4 classes:
      - 0: affected_injured_or_dead_people
      - 1: infrastructure_and_utility_damage
      - 2: not_humanitarian
      - 3: rescue_volunteering_or_donation_effort
    - The `damage_severity` network will classify images into 3 classes:
      - 0: little_or_none
      - 1: mild
      - 2: severe
  - `./resources/twitter-datasets/2018-aude-flood` contains a small dataset collected from [Twitter](https://twitter.com) during 2018 Aude Flood.
    - These datasets are used to test the image processing workflow and build the demo.
    - Raw data of `2018-aude-flood-tweets.json` are provided by [VISOV](https://www.visov.org/).
    - Raw data of `2018-aude-flood-images-from-diego-kozlowski.json` are provided by an [academic article](https://www.sciencedirect.com/science/article/pii/S0306457320300650?via%3Dihub).
- `./src`
  - `./src/twitter_dataset.py` provides functions to fetch a tweet, get the corresponding image, and ask to perform the following processing.
  - `./src/crisis_image_benchmarks_classifier.py` provides functions to classify images into different classes and thus extract related information as labels.
  - `./src/crisis_image_benchmarks_middleware.py` provides functions to transform labels into concepts, that can be used to update the situational model.
  - `./src/rioda_python_driver.py` provides functions to instantiate concepts, in other words, add concepts to R-IODA.
- `./test`
  - Provides several jupyter notebooks to test the functions in `./src`.
- `./demo`

  - Provides a jupyter notebook that can be regard as a demo of 2018 Aude Flood.

