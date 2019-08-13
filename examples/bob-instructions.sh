#!/bin/bash
# Render build instructions from the Bee Observer Project.
# https://community.hiveeyes.org/t/index-dokumentation-fur-bee-observer-nachbau/2455

mkdir -p var/tmp

COMBINED=true
MULTIPLE=true

function render() {
    discodoc --format=pdf --output-path=var/tmp "$@" \
        https://community.hiveeyes.org/t/teileliste-des-bob-hardware-kits/2103 \
        https://community.hiveeyes.org/t/bee-observer-stockwaage-bauen/2457 \
        https://community.hiveeyes.org/t/anleitung-aufbau-und-installation-des-sensor-kits-grune-platine/2443 \
        https://community.hiveeyes.org/t/bee-observer-temperatursensoren-einbauen/2458
}

# Create combined PDF document.
if $COMBINED -eq "true"; then
    render --combine --title="Bee Observer Sensor-Kit Construction Manual"
fi

# Create multiple PDF documents.
if $MULTIPLE -eq "true"; then
    render --enumerate
fi
