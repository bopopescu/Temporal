import random,time
import mysql.connector

class Grind():
    def __init__(self):
        self.count=1
        self.sql_status='pending'


    def read_serial(self):

        #print(self.count)
        if self.count == 1:
            time.sleep(1)
            payload=self.count, time.time()# new event tag
        if self.count==2:
            time.sleep(1.2)
            payload= self.count, random.randint(0,3),random.randint(0,3),random.randint(0,3), random.randint(0,3) #Song
        if self.count == 3:
            time.sleep(random.randint(20,80)/100)
            payload= self.count, time.time()#timestamp
        if self.count == 4:
            time.sleep(1)
            payload= self.count, random.randint(-1, 1),random.randint(0, 1) #right/wrong
        if self.count == 5:
            time.sleep(.1)
            payload= self.count, random.randint(0, 16)
        self.count = self.count + 1 if self.count < 5 else 1
        return payload
# Type 1 Transmission: Session start Session_Id ++
# Type 2 Transmission: End of Phase 1, tone info cdef
# Type 3 Transmission: Event trigger, 1f - left, 1e - right
# Type 4 Transmission: End of Phase 2, lick info, correct/ incorrect info
# Type 5 Transmission: Difficulty
# 1	SequenceStartTime	TIME
# 2	Song	STR
# 3	LickTime	CSV(STR)
# 4	Difficulty	INT
# 5	LickResult	INT
# 6	Correctness	BOOL
def Serial_Process(pcc,idump,lickdump,songdump,timestampd,new_stuff):
    print("thread started")
    # cursor = cnx.cursor()
    # t_zero_que = "INSERT INTO  Temporal_Trails(Session_ID,Animal_ID,Event_Type_ID,Trail_ID,Result) VALUES (%i,%i,%i,%i)"
    event_time = []
    while 1:

        result = pcc.read_serial()
  #      print(result)
        type = result[0]
        if type == 1:
            t_zero = result[1]
            # cursor.execute(t_zero_que, (t_zero,))
            # cnx.commit()
        if type == 2:
            song=result[1:4]
            for i in range(len(song)):
                songdump[i] = song[i]
        if type == 3:
            event_time.append(result[1] - t_zero)
          #  print('Lick time= %f' % event_time[::-1][0])

        if type == 4:  # type==4:
            direction = result[1]
            correct = result[2]

        if type == 5:  # plot difficulty
            difficulty=result[1]

            idump[0]=direction
            idump[1]=correct
            idump[2]=difficulty
            for i in range(len(event_time)):
                lickdump[i]=event_time[i]
            # print(event_time[:])
            # print(lickdump[:])
            timestampd=t_zero
            event_time = []
            new_stuff.value=True
            print("####THREAD##### : Toggled")


