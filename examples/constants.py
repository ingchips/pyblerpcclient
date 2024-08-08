VERDICT = 'VERDICT/'

# PTS State
PTS_IDLE    = 0
PTS_RUNNING = 1
PTS_WAITING = 2
PTS_ABORT = -1

# Verdict strings
RESULT_PASS = 'PASS'
RESULT_FAIL = 'FAIL'
RESULT_INCONC = 'INCONC'
RESULT_INCOMP = 'INCOMP' # Initial final verdict meaning that test has not completed yet
RESULT_NONE = 'NONE' # Error verdict usually indicating internal PTS error

# PTS Log Types:
LOG_TYPE_GENERAL_TEXT           = 0
LOG_TYPE_FIRST                  = 1 # first log type that may be toggled by user
LOG_TYPE_START_TEST_CASE        = 1
LOG_TYPE_TEST_CASE_ENDED        = 2
LOG_TYPE_START_DEFAULT          = 3
LOG_TYPE_DEFAULT_ENDED          = 4
LOG_TYPE_FINAL_VERDICT          = 5
LOG_TYPE_PRELIMINARY_VERDICT    = 6
LOG_TYPE_TIMEOUT                = 7
LOG_TYPE_ASSIGNMENT             = 8
LOG_TYPE_START_TIMER            = 9
LOG_TYPE_STOP_TIMER             = 10
LOG_TYPE_CANCEL_TIMER           = 11
LOG_TYPE_READ_TIMER             = 12
LOG_TYPE_ATTACH                 = 13
LOG_TYPE_IMPLICIT_SEND          = 14
LOG_TYPE_GOTO                   = 15
LOG_TYPE_TIMED_OUT_TIMER        = 16
LOG_TYPE_ERROR                  = 17
LOG_TYPE_CREATE                 = 18
LOG_TYPE_DONE                   = 19
LOG_TYPE_ACTIVATE               = 20
LOG_TYPE_MESSAGE                = 21
LOG_TYPE_LINE_MATCHED           = 22
LOG_TYPE_LINE_NOT_MATCHED       = 23
LOG_TYPE_SEND_EVENT             = 24
LOG_TYPE_RECEIVE_EVENT          = 25
LOG_TYPE_OTHERWISE_EVENT        = 26
LOG_TYPE_RECEIVED_ON_PCO        = 27
LOG_TYPE_MATCH_FAILED           = 28
LOG_TYPE_COORDINATION_MESSAGE   = 29