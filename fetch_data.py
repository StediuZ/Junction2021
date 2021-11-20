{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "aa6ac076-a880-4463-b808-8e4825f2a1fd",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'{\"2021-08-05\": {\"0\": {}, \"1\": {}, \"2\": {\"22\": 640, \"50\": 177, \"53\": 186, \"30\": 965, \"32\": 211, \"34\": 326, \"8\": 323, \"33\": 285, \"36\": 315, \"42\": 102, \"10\": 99, \"13\": 63, \"11\": 35, \"1\": 375, \"29\": 730, \"37\": 237, \"39\": 286, \"31\": 100, \"9\": 75, \"38\": 133, \"40\": 307, \"35\": 51, \"52\": 489, \"23\": 508, \"44\": 217, \"16\": 491, \"12\": 283, \"28\": 696, \"49\": 570, \"0\": 372, \"19\": 256, \"21\": 474, \"48\": 326, \"14\": 480, \"24\": 565, \"27\": 234, \"51\": 198, \"47\": 185, \"41\": 27, \"55\": 187, \"43\": 121, \"20\": 215, \"54\": 207, \"15\": 237, \"18\": 20, \"45\": 99, \"17\": 140, \"46\": 12}, \"3\": {}, \"4\": {}, \"5\": {}, \"6\": {}, \"7\": {}, \"8\": {}, \"9\": {}, \"10\": {}, \"11\": {}, \"12\": {}, \"13\": {}, \"14\": {}, \"15\": {}, \"16\": {}, \"17\": {}, \"18\": {}, \"19\": {}, \"20\": {}, \"21\": {}, \"22\": {}, \"23\": {}}}'"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import base64\n",
    "import imageio as iio\n",
    "from plotting import Plotting\n",
    "import plotly.graph_objects as go\n",
    "import json\n",
    "\n",
    "def fetch_data(site, timestamp)\n",
    "    #site = 'site_1'\n",
    "    #timestamp = \"2021-08-05\"\n",
    "\n",
    "    df_events = pd.read_pickle(f'./data/{site}/{site}.pkl', compression='gzip')\n",
    "    df_events.loc[:, 'timestamp'] = (pd.to_datetime(df_events['timestamp'], utc=True)\n",
    "                                     .dt.tz_convert('Europe/Helsinki')\n",
    "                                     .dt.tz_localize(None))\n",
    "\n",
    "    df_events_test = df_events[df_events.timestamp.dt.date.astype(str) == timestamp].copy()\n",
    "\n",
    "    hour = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']#list(df_events_test['timestamp'].dt.hour.astype(str))\n",
    "    hours = list(df_events_test['timestamp'].dt.hour.astype(str))\n",
    "    device = list(df_events_test['deviceid'])\n",
    "\n",
    "    data = {}\n",
    "    data = {timestamp_min:{}}                              \n",
    "    for i in hour:\n",
    "        data[timestamp_min][i]={}\n",
    "        if(hours[x]==i):\n",
    "            for x in range(0,len(df_events_test)):\n",
    "                if(device[x] in data[timestamp_min][i]):\n",
    "                    data[timestamp_min][i][device[x]]+=1\n",
    "                else:\n",
    "                    data[timestamp_min][i][device[x]]=1\n",
    "\n",
    "    jsonString = json.dumps(data)\n",
    "    return jsonString\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "af23d18d-78e3-440e-aa1e-1de0276947d2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
