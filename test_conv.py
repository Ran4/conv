from conv import conv, Language

def test_conv_json_to_json():
    json_string = '{"name": "foo", "active": false, "redirect_url": null}'
    assert conv(json_string, Language.Json, Language.Json) == json_string


def test_conv_json_to_python():
    json_string = '{"name": "foo", "active": false, "redirect_url": null}'
    assert conv(json_string, Language.Json, Language.Python) == (
        "{'name': 'foo', 'active': False, 'redirect_url': None}"
    )


def test_conv_python_to_json():
    json_string = '{"name": "foo", "active": false, "redirect_url": null}'
    assert conv(json_string, Language.Json, Language.Python) == (
        "{'name': 'foo', 'active': False, 'redirect_url': None}"
    )
