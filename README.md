# My Academic and Professional Profiles

<div style="display: flex; align-items: center; justify-content: center; gap: 20px; text-align: center;">

  <a href="https://scholar.google.com/citations?user=WCqPnS4AAAAJ&hl=en" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Google_Scholar_logo.svg/2048px-Google_Scholar_logo.svg.png" alt="Google Scholar" style="width:40px;height:40px;">
  </a>

  <a href="https://www.researchgate.net/profile/M-Ahsan-Khodami" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/ResearchGate_icon_SVG.svg" alt="ResearchGate" style="width:40px;height:40px;">
  </a>

  <a href="https://github.com/Ahsankhodami" target="_blank">
    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" style="width:40px;height:40px;">
  </a>

  <a href="https://khodami.site" target="_blank">
    <img src="https://www.svgrepo.com/show/474749/broken-link.svg" alt="Website" style="width:40px;height:40px;">
  </a>

</div>
<hr>


# asc2csv
![DOI](https://img.shields.io/badge/DOI-10.31219/osf.io/vfpy5-blue) ![PyPI](https://img.shields.io/pypi/v/asc2csv)

**asc2csv** is a Python package developed for converting EyeLink `.asc` files into structured `.csv` files, facilitating the analysis of eye-tracking data. It extracts gaze data and event details such as blinks, saccades, and fixations, organizing them into an easy-to-use format.

</p>

**asc2csv** is a Python package developed for converting EyeLink `.asc` files into structured `.csv` files, facilitating the analysis of eye-tracking data. It extracts gaze data and event details such as blinks, saccades, and fixations, organizing them into an easy-to-use format.


## Features
- Converts EyeLink `.asc` files to `.csv` format efficiently.
- Extracts and processes blink (`EBLINK`), saccade (`ESACC`), and fixation (`EFIX`) event data.
- Aligns timestamps relative to trial start for consistent temporal analysis.
- Handles missing data by combining event and sample data fields where applicable.

## **Changelog**

<details>
  <summary>See the Changes in versions</summary>

### **Version 1.4**
- Initial release of `asc2csv`.
- V 1.4 Update 12/11/24   make adding `header=True` in conversion optional. By default `header=True` is applied.

### **Version 1.4.1**
- Enhanced data importing

</details>


## Installation

To install the package, run:

```bash
pip install asc2csv
```

## Usage

Import the package and use the `process_asc_file()` function:

```python
import asc2csv as convert

convert.process_asc_file('input_file.asc', 'output_file.csv')
```

### Parameters
- **`input_file_path`** (str): Path to the input `.asc` file.
- **`output_csv_path`** (str): Path to save the output `.csv` file.
- **`header`** (bool, optional): Whether to include a header row in the output CSV. Default is `True`.

## Requirements
- Python >= 3.6
- `pandas`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! If you find a bug or have an idea for an improvement, please submit a pull request or open an issue.

## Creator and Maintainer

**Mohammad Ahsan Khodami**  
- Personal Site: [khodami.site](https://khodami.site)  
- Google Scholar: [Profile](https://scholar.google.com/citations?user=WCqPnS4AAAAJ&hl=en)  
- Email: [ahsan.khodami@gmail.com](mailto:ahsan.khodami@gmail.com)

## Acknowledgments
- The EyeLink system and data format are provided by SR Research.