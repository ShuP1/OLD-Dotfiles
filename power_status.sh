#!/bin/sh
# use notify-send to prompt power status
# and hibernate on critical level (< 3%)

last_capacity=100
last_status="Charging"
while true
do
    sleep 10
    status=$(acpi -b | awk -F'[,:%]' '{print $2}')
    capacity=$(acpi -b | awk -F'[,:%]' '{print $3}')
    if [ $status != $last_status ]; then
        last_status=$status
        notify-send -a "Power Status" "Power mode change" $status
    fi
    if [ $status = "Discharging" ]; then
        if [ "$capacity" -lt "$last_capacity" ]; then
            last_capacity=$capacity
	    if [ "$capacity" -eq 15 ] || [ "$capacity" -eq 10 ] || [ "$capacity" -le 5 ]; then
                notify-send -a "Power Status" -u critical "Low battery" "$capacity% left !"
            fi
        fi
        if [ "$capacity" -lt 3 ]; then
            logger "Critical battery level"
            systemctl hibernate
        fi
    fi
done
