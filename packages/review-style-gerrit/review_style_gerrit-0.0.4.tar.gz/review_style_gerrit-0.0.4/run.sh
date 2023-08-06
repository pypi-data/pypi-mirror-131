current_path=$(pwd)
cd /home/tom/tmp/sample2

export GERRIT_USER=gerritadmin
export GERRIT_PASSWORD=ew2wYTsrEOi5HoV71YKwSs3RL77nKj

python3 $current_path/runner.py http://review.firmenessen.de/sample2
