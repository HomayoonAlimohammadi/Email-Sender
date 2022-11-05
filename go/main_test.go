package main

import (
	"testing"

	"gopkg.in/gomail.v2"
)

type SenderMock struct {
	Calls int
	Msg   *gomail.Message
}

func (mock *SenderMock) Send(msg *gomail.Message) {
	mock.Calls++
}

func NewSenderMock() *SenderMock {
	return &SenderMock{}
}

func TestSendEmail(t *testing.T) {

}
