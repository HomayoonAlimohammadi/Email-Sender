.PHONY: py pydeps go godeps gobuild help check_files

BINARY_OUTPUT := EmailSender
EXE_OUTPUT := EmailSender.exe

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
	go build -o ${BINARY_OUTPUT} main.go

gobuild_win: godeps
	cd go && \
	env GOOS=windows GOARCH=amd64 go build -o ${EXE_OUTPUT} main.go

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
	find . -name '*${BINARY_OUTPUT}' -delete
	find . -name '*${EXE_OUTPUT}' -delete