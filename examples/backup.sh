#!/usr/bin/env bash
fifo=../bin/fifo
vm="$2"
case $1 in
    monthly)
        $fifo vms backups $vm create monthly
        last_daily=$($fifo vms backups $vm list -pH --fmt uuid,comment | grep 'daily' | grep 'YES' | tail -1)
        if [ ! -z "$last_daily" ]
        then
            daily_uuid=$(echo $last_daily | cut -d: -f1)
            $fifo vms backups $vm delete -l $daily_uuid
        fi
        last_weekly=$($fifo vms backups $vm list -pH --fmt uuid,comment | grep 'weekly' | grep 'YES' | tail -1)
        if [ ! -z "$last_weekly" ]
        then
            weekly_uuid=$(echo $last_weekly | cut -d: -f1)
            $fifo vms backups $vm delete -l $weekly_uuid
        fi
        ;;
    weekly)
        last_backup=$($fifo vms backups $vm list -pH --fmt uuid,comment | grep 'monthly\|weekly' | grep 'YES' | tail -1)
        uuid=$(echo $last_backup | cut -d: -f1)
        type=$(echo $last_backup | cut -d: -f2)
        $fifo vms backups $vm create --parent $uuid -d weekly
        last_daily=$($fifo vms backups $vm list -pH --fmt uuid,comment | grep 'daily' | grep 'YES' | tail -1)
        if [ ! -z "$last_daily" ]
        then
            daily_uuid=$(echo $last_daily | cut -d: -f1)
            $fifo vms backups $vm delete -l $daily_uuid
        fi
        ;;
    daily)
        last_backup=$($fifo vms backups $vm list -pH --fmt uuid,comment | grep 'daily\|weekly' | grep 'YES' | tail -1)
        uuid=$(echo $last_backup | cut -d: -f1)
        type=$(echo $last_backup | cut -d: -f2)
        case $type in
            weekly)
                $fifo vms backups $vm create --parent $uuid daily
                ;;
            daily)
                $fifo vms backups $vm create --parent $uuid -d daily
                ;;
        esac
        ;;
esac
