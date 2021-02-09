+++
title = "A Simple Go JSON API Server with Tests"
date = 2018-12-10
updated = 2018-12-10
aliases = [ "2018/12/10/A-Simple-Go-JSON-API-Server-with-Tests.html" ]
+++

I'm trying to make a small bookmarks server. I'm using code similar to this to create a server, and test 2 GET APIs.
I'm incorporating  the following ideas from [Advanced Testing in Go](https://about.sourcegraph.com/go/advanced-testing-in-go):
- Subtests/Table driven tests
- Golden files
- Test fixtures

I'm not sure this code is exactly what I want, but I do think its' a good starting place:

### main.go

```go
package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/julienschmidt/httprouter"
)

// NormalizedColumn is the json structure
type NormalizedColumn struct {
	ID   int64  `json:"id"`
	Name string `json:"name"`
}

// NewServer returns a server to serve from
func NewServer() (*Server, error) {
	data1 := []NormalizedColumn{
		{1, "one"},
		{2, "two"},
	}
	data2 := []NormalizedColumn{
		{3, "three"},
		{4, "four"},
	}
	return &Server{data1, data2}, nil
}

// Server that has data to use
type Server struct {
	data1 []NormalizedColumn
	data2 []NormalizedColumn
}

func (s *Server) getData1(w http.ResponseWriter, req *http.Request, _ httprouter.Params) {
	w.Header().Set("Content-Type", "application/json")
	e := json.NewEncoder(w)
	e.SetIndent("", "  ") // NOTE: pretty-printing might not be good on an API
	e.Encode(s.data1)

}

func (s *Server) getData2(w http.ResponseWriter, req *http.Request, _ httprouter.Params) {
	w.Header().Set("Content-Type", "application/json")
	e := json.NewEncoder(w)
	e.SetIndent("", "  ") // NOTE: pretty-printing might not be good on an API
	e.Encode(s.data2)

}

func main() {
	s, err := NewServer()
	if err != nil {
		log.Fatal(err)
	}

	router := httprouter.New()
	router.GET("/getData1", s.getData1)
	router.GET("/getData2", s.getData2)

	log.Fatal(http.ListenAndServe(":8080", router))
}
```

### main_test.go

```go
package main

import (
	"bytes"
	"flag"
	"io/ioutil"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"

	"github.com/julienschmidt/httprouter"
)

// https://medium.com/@povilasve/go-advanced-tips-tricks-a872503ac859

var update = flag.Bool("update", false, "update .golden files")

// TestGetDatas tests all GET REST APIs
func TestGetDatas(t *testing.T) {

	// Create Server
	s, err := NewServer()
	if err != nil {
		t.Fatalf("Server Error: %+v\n", err)
	}

	// Create cases
	cases := []struct {
		testName     string
		serverMethod httprouter.Handle
		httpMethod   string
		urlPath      string
	}{
		{"getData1", s.getData1, "GET", "/getData1"},
		{"getData2", s.getData2, "GET", "/getData2"},
	}

	for _, tt := range cases {
		t.Run(tt.testName, func(t *testing.T) {

			// Record request to server
			req := httptest.NewRequest(tt.httpMethod, tt.urlPath, nil)
			w := httptest.NewRecorder()
			tt.serverMethod(w, req, nil)

			resp := w.Result()
			body, err := ioutil.ReadAll(resp.Body)

			// Test common things

			if resp.StatusCode != http.StatusOK {
				t.Errorf("Status Code: %#v != http.StatusOK: %#v\n", resp.StatusCode, http.StatusOK)
			}

			contentType := resp.Header.Get("Content-Type")
			if contentType != "application/json" {
				t.Errorf("Content-Type: %#v != 'application/json'", contentType)
			}

			// Test body from golden file

			testDir := "testdata"

			golden := filepath.Join(testDir, tt.testName+".golden.json")
			if *update {
				err := os.MkdirAll(testDir, 0755)
				if err != nil {
					t.Fatalf("Mkdir Failure: %#v\n", err)
				}
				ioutil.WriteFile(golden, body, 0644)
			} else {
				if _, err := os.Stat(testDir); os.IsNotExist(err) {
					t.Fatalf("Run `go test -update` to create the test data")
				}
			}

			expected, err := ioutil.ReadFile(golden)
			if err != nil {
				if err != nil {
					t.Fatalf("ReadFile Failure: %#v\n", err)
				}
			}

			if !bytes.Equal(body, expected) {
				t.Logf("Actual:\n%#v", body)
				t.Logf("Expected:\n%#v", expected)
				t.Fail()
			}
		})
	}
}
```
