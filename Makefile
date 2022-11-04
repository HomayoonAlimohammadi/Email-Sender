.PHONY: py pydeps go godeps gobuild help check_files

py: pydeps
	cd python && \
	python3 email_sender.py

pydeps:
	cd python && \
	pip install -r requirements.txt -q \

go: godeps
	cd go && \
	go run main.go

gobuild: godeps
	cd go && \
	go build -o EmailSender main.go

gobuild_win: godeps
	cd go && \
	go build -o EmailSender.exe main.go

godeps:
	cd go && \
	go mod download

help:
	@echo "\033[0;36mMade with <3 by Homayoon Alimohammadi \033[0;37m"
	@echo "This is the EmailSender Project"
	@echo "It's implemented in two versions, one in Python and the other one in Golang."
	@echo "Head to the README.md in order order to learn how to run each version"

clean:
	find . -wholename '*/exported/*' -delete 
	find . -name '*EmailSender' -delete
	find . -name '*EmailSender.exe' -delete