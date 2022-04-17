#!/bin/bash

prompt(){
    echo -e "\e[4mChoose Program:\e[0m\n 1: \e[35mHuman Detection\e[39m \t 2: \e[36mVehicle Detection\e[39m \t 3: \e[34mRoadlane Detection\e[39m"
    read -p 'Input: ' num
}

while (true); do

    prompt

    if [[ $num == '1' ]]; then
        python3 human-detect.py 2> /dev/null
    elif [[ $num == '2' ]]; then
        python3 vehicle_detect.py 2> /dev/null
    elif [[ $num == '3' ]]; then
        python3 roadlane.py 2> /dev/null
    elif [[ $num == 'q' ]]; then
        exit 0
    fi

done

