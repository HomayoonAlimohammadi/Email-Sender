package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"math"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/joho/godotenv"
	"github.com/k3a/html2text"
	"github.com/xuri/excelize/v2"
	"gopkg.in/gomail.v2"
)

var waitGroup sync.WaitGroup

// MyData struct that contains the main configuration
// from my_data.json
type MyData struct {
	Email      string `json:"email"`
	Password   string `json:"password"`
	FirstName  string `json:"first_name"`
	LastName   string `json:"last_name"`
	City       string `json:"city"`
	Country    string `json:"country"`
	Major      string `json:"major"`
	University string `json:"university"`
	Gpa        string `json:"gpa"`
	Toefl      string `json:"toefl"`
	Website    string `json:"website"`
}

// ProfessorData struct that will contain each professor's data
type ProfessorData struct {
	FirstName       string `json:"first_name"`
	LastName        string `json:"last_name"`
	Interest        string `json:"interest"`
	FirstPaper      string `json:"first_paper"`
	FirstPaperYear  string `json:"first_paper_year"`
	SecondPaper     string `json:"second_paper"`
	SecondPaperYear string `json:"second_paper_year"`
	University      string `json:"university"`
	TargetDegree    string `json:"target_degree"`
	Email           string `json:"email"`
}

// EmailSender struct which will be initialized and used
// to send emails
type EmailSender struct {
	Email    string         `json:"email"`
	Password string         `json:"password"`
	Host     string         `json:"host"`
	Port     int            `json:"port"`
	Address  string         `json:"address"`
	Dialer   *gomail.Dialer `json:"auth"`
}

// Given the "email" and "passowrd", will return a pointer to an
// EmailSender object.
// Use this to instanciate and initialize EmailSender objects.
func NewEmailSender(email, password string) *EmailSender {
	host := "smtp.gmail.com"
	port := 587
	dialer := gomail.NewDialer(host, port, email, password)
	return &EmailSender{
		Email:    email,
		Password: password,
		Host:     host,
		Port:     port,
		Dialer:   dialer,
	}
}

// Given sufficient information for a valid email, creates a Message and sends it.
func (es *EmailSender) CreateAndSendEmailMessage(to, subject, emailContent, attachmentPath string) error {
	msg := gomail.NewMessage()
	msg.SetHeader("From", es.Email)
	msg.SetHeader("To", to)
	msg.SetHeader("Subject", subject)
	msg.SetBody("text/html", emailContent)
	msg.Attach(attachmentPath)
	if err := es.Dialer.DialAndSend(msg); err != nil {
		return err
	}
	return nil
}

// Given the path to my_data.json, loads it and returns an instance of MyData.
func loadMyData(path string) (MyData, error) {
	var myData MyData
	f, err := ioutil.ReadFile(path)
	if err != nil {
		return MyData{}, err
	}
	err = json.Unmarshal(f, &myData)
	if err != nil {
		return MyData{}, err
	}
	return myData, nil
}

// Given the path to email_content.txt, loads it and returns a string.
func loadEmailContent(path string) (string, error) {
	file, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer func() {
		if err := file.Close(); err != nil {
			log.Fatalln("\033[0;31m error closing email_content.txt file: \033[0;37m", err)
		}
	}()

	content, err := ioutil.ReadAll(file)
	if err != nil {
		return "", err
	}

	return string(content), nil
}

// Given the path to professors.xlsx, loads it and returns a slice of ProfessorData(s).
func loadAllProfsData(path string) ([]ProfessorData, error) {
	file, err := excelize.OpenFile(path)
	if err != nil {
		return []ProfessorData{}, err
	}
	defer func() {
		if err := file.Close(); err != nil {
			log.Fatalln("\033[0;31m error closing professors.xlsx file: \033[0;37m", err)
		}
	}()

	sheets := file.GetSheetList()
	rows, err := file.GetRows(sheets[0])
	var allProfData []ProfessorData
	if err != nil {
		return []ProfessorData{}, err
	}
	for _, row := range rows[1:] {
		allProfData = append(allProfData, ProfessorData{
			FirstName:       row[0],
			LastName:        row[1],
			Interest:        row[2],
			FirstPaper:      row[3],
			FirstPaperYear:  row[4],
			SecondPaper:     row[5],
			SecondPaperYear: row[6],
			University:      row[7],
			TargetDegree:    row[8],
			Email:           row[9],
		})
	}
	return allProfData, nil
}

// Given an email content string and a fileName, exports the text to the file.
func exportEmailContent(text, fileName string) error {
	path := "./exported/"
	_, err := os.Stat(path)
	if os.IsNotExist(err) {
		os.Mkdir("exported", os.ModePerm)
	} else if err != nil {
		return err
	}
	file, err := os.Create(path + fileName)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.WriteString(text)
	if err != nil {
		return err
	}
	log.Println("\033[0;32m successfullly exported to: \033[0;37m", fileName)
	return nil
}

// Given the email content template and sufficient data, renders the template and returns the final string.
// An export parameter will be used to indicate whether or not the final text will be exported.
func renderEmailContent(emailContentTemplate string, myData MyData, profData ProfessorData, export bool) string {
	replacer := strings.NewReplacer(
		"{prof_last_name}", profData.LastName,
		"{my_first_name}", myData.FirstName,
		"{my_last_name}", myData.LastName,
		"{my_major}", myData.Major,
		"{my_university}", myData.University,
		"{my_city}", myData.City,
		"{my_country}", myData.Country,
		"{my_gpa}", myData.Gpa,
		"{my_toefl}", myData.Toefl,
		"{prof_interest}", profData.Interest,
		"{prof_first_paper}", profData.FirstPaper,
		"{prof_first_paper_year}", profData.FirstPaperYear,
		"{prof_second_paper}", profData.SecondPaper,
		"{prof_second_paper_year}", profData.SecondPaperYear,
		"{target_degree}", profData.TargetDegree,
		"{prof_university}", profData.University,
		"{my_website}", myData.Website,
	)
	emailContentHtml := replacer.Replace(emailContentTemplate)
	emailContentText := html2text.HTML2Text(emailContentHtml)

	// Export emailContent
	if export {
		fileName := profData.University + "_" + string(profData.FirstName[0]) + "_" + profData.LastName
		err := exportEmailContent(emailContentText, fileName)
		if err != nil {
			log.Println("\033[0;31m error exporting email content: \033[0;37m", err)
		}
	}

	return emailContentHtml
}

// Given the base email subject and sufficient data, returns the final subject string.
func renderSubject(baseSubject string, profData ProfessorData) string {
	replacer := strings.NewReplacer(
		"{interest}", profData.Interest,
	)
	return replacer.Replace(baseSubject)
}

// Given a pointer to an instance of EmailSender, with subject and email content templates and sufficient data,
// renders the final subject and email content, then sends appropriate email to each professor.
// export and confirmSend parameters are used to indicate whether the final text will be exported into a .txt file
// and whether the prepared email is actually sent (set the confirmSend to false for development and test purposes).
func sendEmailToAllProfessors(emailSender *EmailSender, baseSubject, emailContentTemplate, attachmentPath string, myData MyData, allProfsData []ProfessorData, exportAllEmailContent, confirmSend bool) error {
	for _, profData := range allProfsData {
		emailContent := renderEmailContent(emailContentTemplate, myData, profData, exportAllEmailContent)

		if confirmSend {
			subject := renderSubject(baseSubject, profData)
			to := profData.Email
			waitGroup.Add(1)
			go func(to, subject, emailContent, attachmentPath string) {
				err := emailSender.CreateAndSendEmailMessage(
					to,
					subject,
					emailContent,
					attachmentPath,
				)
				if err != nil {
					log.Fatalln("\033[0;31m error sending email to all professors: \033[0;37m", err)
				}
				waitGroup.Done()

			}(to, subject, emailContent, attachmentPath)
			log.Println("\033[0;32m successfully sent email to: \033[0;37m", to)
		}
	}
	return nil
}

func main() {

	log.Println("\033[0;36m Made with <3 by Homayoon Alimohammadi \033[0;37m")

	t0 := time.Now()

	err := godotenv.Load("../.env")
	if err != nil {
		log.Fatalln("\033[0;31m error loading .env file: \033[0;37m", err)

	}

	myDataPath := "../my_data.json"
	emailContentTemplatePath := "../email_content.txt"
	allProfsDataPath := "../professors.xlsx"
	attachmentPath := "../Resume.pdf"
	exportAllEmailContent := os.Getenv("EXPORT_CONTENT") == "1"
	confirmSend := os.Getenv("SEND_EMAIL") == "1"
	baseSubject := "Prospective student interested in {interest} with Machine Learning background"

	// Load myData
	myData, err := loadMyData(myDataPath)
	if err != nil {
		log.Fatalln("\033[0;31m error loading my_data.json: \033[0;37m", err)
	}

	// Load emailContent
	emailContentTemplate, err := loadEmailContent(emailContentTemplatePath)
	if err != nil {
		log.Fatalln("\033[0;31m error loading email_content.txt: \033[0;37m", err)
	}

	// Load allProfsData
	allProfsData, err := loadAllProfsData(allProfsDataPath)
	if err != nil {
		log.Fatalln("\033[0;31m error loading professors.xlsx: \033[0;37m", err)
	}

	log.Println("\033[0;32m successfully loaded all the necessary data \033[0;37m")

	// Initialize EmailSender
	emailSender := NewEmailSender(myData.Email, myData.Password)
	log.Println("\033[0;32m successfully initialized EmailSender \033[0;37m")
	err = sendEmailToAllProfessors(
		emailSender,
		baseSubject,
		emailContentTemplate,
		attachmentPath,
		myData,
		allProfsData,
		exportAllEmailContent,
		confirmSend,
	)
	if err != nil {
		log.Fatalln("\033[0;31m error sending email to all professors: \033[0;37m", err)
	}
	waitGroup.Wait()
	log.Println("\033[0;32m successfully sent email to all professors! \033[0;37m")
	t1 := time.Now()
	log.Println("\033[0;36m Elapsed time: \033[0;37m", math.Round(t1.Sub(t0).Seconds()*100)/100)
}
