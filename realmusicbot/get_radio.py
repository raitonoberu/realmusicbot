from pyradios import RadioBrowser
rb = RadioBrowser()


def get_radio(radio_title):
    stantions = rb.stations_by_name(radio_title)
    if stantions != []:
        stantion = sorted(
            stantions, key=lambda k: k['votes'], reverse=True)[0]
        return {"title": stantion['name'], "duration": "radio",
                "file": stantion['url_resolved'], "cover": None}
    else:
        return {}
