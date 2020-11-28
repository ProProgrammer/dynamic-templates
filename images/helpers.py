def update_url_and_text_in_template(template: dict, url: str, text: str) -> dict:
    """
    Given strings, `url` and `text`, set URL and text in the `template`

    Sample Template:
        {'height': 600,
         'objects': [{'height': 300,
                      'type': 'image',
                      'url': '',
                      'width': 350,
                      'x': 300,
                      'y': 300},
                     {'height': 100,
                      'text': '',
                      'type': 'textbox',
                      'width': 300,
                      'x': 400,
                      'y': 300}],
         'width': 600}

    Returns: Dictionary reflecting updated template
    """
    for item in list(template.values()):
        try:
            for record in item:
                if record.get('type') == 'image':
                    record['url'] = url
                elif record.get('type') == 'textbox':
                    record['text'] = text
        except TypeError:
            pass

    return template


def generate_data_templates_from_csv_data(csv_file, template) -> None:
    """
    Given CSV file, iterate over the data and generate final template that can be used as request body for IGS API

    The final template must be stored in `Template` Django model since storing them in memory can cause out of memory
    issues for large data sets.
    """
    pass


def process_data_templates():
    """
    Fetch unprocessed templates (`Template` object) and process them with IGS API
    If the API return status OK, mark the template as processed.
    """
    pass

# Introduce polling mechanism that checks if there's new CSV
# Seek clarification - In case of new data, will existing CSV be updated with new data or will new CSVs be uploaded?
# If new CSV, it becomes easy, as we can simply store in cache which was the last CSV processed and constantly check
# if the most recent CSV is different than the last CSV.

