from mdslaremote import mda
import threading
import time
import datetime

xml="<nodeConfig>1 - AMR-WB 0/0-8 20 ms POLQA -18 dBm<configParam name='Type' value='SIP' /><configParam name='CallProgress' value='True' /><configParam name='Port' value='5060' /><configParam name='SignInName' value='+445600680768' /><configParam name='SignInDomain' value='10.18.69.126' /><configParam name='UserAgent' value='' /><configParam name='P_AssertedId' value='1' /><configParam name='PublicIP' value='' /><configParam name='CodecFamily' value='AMR' /><configParam name='SampleRate' value='16000' /><configParam name='CodecBitRate' value='6.6;8.85;12.65;14.25;15.85;18.25;19.85;23.05;23.85' /><configParam name='PayloadFormat' value='Octet Aligned' /><configParam name='ModeChangePeriod' value='False' /><configParam name='Dtx' value='False' /><configParam name='InitialCmr' value='0' /><configParam name='FrameSize' value='20' /><configParam name='CallControlType' value='None' /><configParam name='AfterDialWait' value='0' /><configParam name='CallDisconnectWait' value='0' /><configParam name='SaveCallHistory' value='True' /><configParam name='InNumCountry(0)' value='' /><configParam name='InNumArea(0)' value='' /><configParam name='InNumNumber(0)' value='+445600680768@10.91.10.122' /><configParam name='CallPreference' value='Signin Name' /><configParam name='ServerAddress' value='10.91.10.122' /><configParam name='ServerUsername' value='' /><configParam name='ServerPassword' value='' /><configParam name='ServerExpiresPeriod' value='3600' /><configParam name='Ims' value='False' /><configParam name='SendInitialAuthorization' value='False' /><configParam name='AlertIDs' value='' /><configParam name='SuppressAlerts' value='False' /><configParam name='Model' value='Wideband' /><configParam name='LevelAlignment' value='True' /><configParam name='PolqaAlgorithmVersion' value='v2' /><configParam name='LowNoisePowerExtn' value='True' /><configParam name='MapPESQLQ' value='True' /><configParam name='DTMFCriteria' value='Default' /><configParam name='ReferenceEQ' value='' /><configParam name='BandwidthDetection' value='True' /><configParam name='MeasuringSampleRate' value='16000' /><configParam name='JitterBuffer' value='150' /><configParam name='NetworkVppQOS' value='None' /><configParam name='DTMFMode' value='RFC2833' /><configParam name='LevelOffset' value='-18' /><configParam name='InputEQ' value='' /><configParam name='OutputEQ' value='' /><configParam name='AbsoluteStart' value='True' /><configParam name='Loopback' value='False' /><configParam name='TrustedOffset' value='False' /><configParam name='ServerRegistration' value='True' /><configParam name='DisableRegister' value='True' /></nodeConfig>"

def main():
    # Set name of Shark object
    threads = []

    start = time.time()
    # Create all the worker threads
    for i in range(0, 3):
        threads.append(threading.Thread(target=run_job, args=(i,)))
        threads[i].start()
        time.sleep(1)

    # Let the threads finish before exiting
    for i in threads:
        i.join()
    end = time.time()
    print('processing time is {}'.format(end-start))

def intFromStr(s):
    try:
        return int(s)
    except ValueError:
        return -1


def run_job(i):
    print('starting job {} in {}'.format(i, datetime.datetime.now()))
    starts.append(datetime.datetime.now())

    #tasklist = 'User Tasklists\\quickqualitychk_adn.mtl'
    tasklist = 'P.501C/EN/Up to 14kHz SWB/quickqualitychk.mtl'
    nodeA = srcNodes[i]
    nodeB = dstNodes[i]

    conn = (nodeA+nodeB).replace(' ', '')
    print(mda.removeconnection(conn))
    connSet = mda.addconnection(conn, nodeA, 'default', nodeB, 'default')
    print('connectionSet : {}'.format(connSet))
    if connSet.startswith('ERROR'):
        exit(1)

    testid = mda.scheduletest(tasklist, conn, "1", "1", "1", mda.NOW)

    #testid = mda.scheduletest(tasklist, nodeA, nodeB, "1", "1", "1", mda.NOW)

    print('test ID : {}'.format(testid))

    if intFromStr(testid) != -1:
        while True:
            time.sleep(3)
            progress = mda.gettestprogress(testid)
            if progress == 'FINISHED':
                now = datetime.datetime.now()
                print('Date {}, TestId {}, Finished.'.format(str(now), testid))
                break
            else:
                if progress == 'FAILED':
                    print('Ending job {} Test {} is failed'.format(i, testid))
                    return
                else:
                    print('TestId {}, Test status: {}'.format(testid, progress))
        #print(mda.getresultlist(testid))
        #print(mda.gettestsummary(testid, mda.BYNODE))
        # print(mda.gettestsummary(testid, 230))
        #print(mda.getresultlist(testid, 'PESQ', 'LEVELS' , 'DELAY', 'ECHO'))
        pesqResult = mda.getresultlist(testid, 'PESQ')
        elapsed = datetime.datetime.now() - starts[i - 1]
        print('PESQ results are : {}'.format(pesqResult))
        polqaResult = mda.getresultlist(testid, 'POLQA')
        print('POLQA results are : {}'.format(polqaResult))
        visqolResult = mda.getresultlist(testid, 'VISQOL')
        print('VISQOL results are : {}'.format(visqolResult))
        #profileResult = mda.getresultlist()
        #levelResults = mda.getresultlist(testid, 'LEVELS')
        #print('LEVEL results are : {}'.format(levelResults))
        #delayResults = mda.getresultlist(testid, 'DELAY')
        #print('DELAY results are : {}'.format(delayResults))
        print('Ending job {} resultid is {}. Finished in {} seconds'.format(i, testid, elapsed.seconds))
    else:
        print('Error starting test : {}'.format(testid))

if __name__ == "__main__":
    starts = []
    srcNodes = ['vpp 1', 'vpp 3', 'vpp 7']
    dstNodes = ['vpp 2', 'vpp 4', 'vpp 8']
    mda.verbose(False)
    #srcNodes = ['vpp 1', 'vpp 3', 'vpp 5', 'vpp 7', 'vpp 9', 'vpp 11', 'vpp 13', 'vpp 15', 'vpp 17']
    #dstNodes = ['vpp 2', 'vpp 4', 'vpp 6', 'vpp 8', 'vpp 10', 'vpp 12', 'vpp 14', 'vpp 16', 'vpp 18']
    logonsuccess = mda.logon("localhost")
    print(logonsuccess)
    if logonsuccess != 'OK':
        exit(1)

    res = mda.loadconfig("vpp 1",  xml)
    #res = mda.getnodelist()
    print(res)
    #res = mda.getgroups()
    #print(res)
    exit(0)
    main()
    mda.logoff()