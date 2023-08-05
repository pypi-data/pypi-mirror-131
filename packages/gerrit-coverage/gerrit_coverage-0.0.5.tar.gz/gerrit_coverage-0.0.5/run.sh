current_path=$(pwd)
cd /home/tom/tmp/sample

export GERRIT_USER=gerritadmin
export GERRIT_PASSWORD=ew2wYTsrEOi5HoV71YKwSs3RL77nKj

#python3 $current_path/check_missing_lines.py http://review.firmenessen.de/sample
python3 $current_path/check_style.py http://review.firmenessen.de/sample
