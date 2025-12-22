from mercury.plugin_loader import discover_plugins, load_manifest


def test_discover_example_plugin():
    plugins = discover_plugins()
    # Use lowercase to avoid case issues
    names = [p['name'].lower() for p in plugins]
    assert 'example_simulator' in names


def test_manifest_local_only():
    plugins = discover_plugins()
    # Case-insensitive match
    p = next((p for p in plugins if p['name'].lower() == 'example_simulator'), None)
    assert p is not None

    manifest = load_manifest(p['path'])
    # Check network_policy exists and is 'local-only'
    assert manifest.get('network_policy') == 'local-only'

def test_manifest_responsible_use():
    plugins = discover_plugins()
    p = next((p for p in plugins if p['name'].lower() == 'example_simulator'), None)
    assert p is not None

    manifest = load_manifest(p['path'])
    assert 'responsible_use' in manifest
    assert isinstance(manifest['responsible_use'], str)

def test_manifest_version():
    plugins = discover_plugins()
    p = next((p for p in plugins if p['name'].lower() == 'example_simulator'), None)
    assert p is not None

    manifest = load_manifest(p['path'])
    assert 'version' in manifest
    assert isinstance(manifest['version'], str)
