from datetime import date
import pandas as pd
import json
import os


class FBTracking:
    def __init__(self, gc, url, sh, worksheet, specialist):
        self.gc = gc
        self.url = url
        self.sh = sh
        self.worksheet = worksheet
        self.specialist = specialist

    def find_unanswered(self):
        df = pd.DataFrame(self.worksheet.get_all_records())
        df = df[["Conversation", "Timestamp (ms)", "Sender"]]
        last_message_time = df.groupby(["Conversation"])["Timestamp (ms)"].max()

        sender = []
        for value in last_message_time[1:]:
            row = df.loc[df["Timestamp (ms)"] == value]
            sender.append(row["Sender"].values[0])

        unanswered_message_count = len(sender) - sender.count(self.specialist)

        return unanswered_message_count

    def value_counts_df(self):
        df = pd.DataFrame(self.worksheet.get_all_records())
        messages = df.groupby(["Message"]).count()["Conversation"]
        message_counts = (
            messages.to_frame()
            .sort_values(by="Conversation", ascending=False)
            .reset_index()
        )
        message_counts["Date"] = date.today()
        message_counts["Account"] = self.specialist

        return message_counts

    def average_per_conversation(self):
        df = pd.DataFrame(self.worksheet.get_all_records())
        df = df[df["Timestamp (ms)"].str.strip().astype(bool)]
        df["Timestamp Int"] = df["Timestamp (ms)"].astype(int)

        timestamp_df = df.groupby(["Conversation", "Timestamp Int"])[
            "Timestamp (ms)"
        ].unique()

        name_dict = {
            name: []
            for name in sorted(list(set([name for name in df["Conversation"]])))
            if name
        }

        average_time_dict = {name: "" for name in name_dict if name}

        for name in name_dict:
            name_dict[name] = timestamp_df[name].astype(int).tolist()

        for name in name_dict:
            s_difference = 0
            for index, time in enumerate(name_dict[name]):
                if index + 1 == len(name_dict[name]):
                    pass
                else:
                    ms_difference = abs(
                        name_dict[name][index] - name_dict[name][index + 1]
                    )
                    s_difference += round(ms_difference / 60000)
            if len(name_dict[name]) < 2:
                del average_time_dict[name]
            else:
                convo_avg = round(s_difference / (len(name_dict[name]) - 1), 2)
                average_time_dict[name] = convo_avg

        average_time_df = (
            pd.DataFrame.from_dict(average_time_dict, orient="index")
            .reset_index()
            .rename(columns={"index": "Conversation Name", 0: "Time To Reply (m)"})
        )

        average_time_df["Date"] = date.today()
        average_time_df["Account"] = self.specialist

        return average_time_df

    def average_of_all_conversations(self):
        average_time_df = self.average_per_conversation()
        return round(average_time_df[average_time_df.columns[1]].mean(), 2)


class Conversion:
    def __init__(self, gc, sh, worksheet, specialist):
        self.gc = gc
        self.sh = sh
        self.worksheet = worksheet
        self.specialist = specialist

    def create_dict(self, data):

        messages = data["messages"]
        conversation_list = []
        newdict = {"Conversation": "", "Sender": "", "Message": "", "Timestamp": ""}
        for message in messages:
            newdict["Conversation"] = data["title"]
            newdict["Sender"] = message["sender_name"]
            newdict["Timestamp"] = message["timestamp_ms"]
            try:
                newdict["Message"] = message["content"]
            except KeyError:
                print(
                    "There was a Key Error, this means the content was either a stick or an emoji"
                )

            conversation_list.append(newdict.copy())

        return conversation_list

    def get_filepaths(self):
        filelist = []
        main_path = "/Users/" + os.environ["USER"] + "/Downloads/messages/inbox/"
        for folder in os.listdir(main_path):
            if folder.endswith(".DS_Store"):
                pass
            else:
                for filename in os.listdir(main_path + folder):
                    if filename.endswith(".json"):
                        filelist.append(main_path + folder + "/" + filename)

        return filelist

    def convert_json(self, filelist):
        message_dictionary = []
        for path in filelist:
            with open(path) as f:
                data = json.load(f)
                message_dictionary.append(self.create_dict(data))

        return message_dictionary

    def create_dataframe(self, message_dictionary):

        df = pd.DataFrame()
        for conversation in message_dictionary:
            df = df.append(pd.DataFrame(conversation), ignore_index=True)

        return df


class Leaderboard:
    def __init__(self, gc, sh, worksheet):
        self.gc = gc
        self.sh = sh
        self.worksheet = worksheet

    def create_dfs(self):

        df = pd.DataFrame.from_dict(self.worksheet.get_all_records())
        df.set_index("Totals | Daily Average", inplace=True)
        df = df["Week Total"]

        pod_names = ["Girls SS", "No_name SS"]
        snr_specialist_names = [
            "Morgan SS",
            "Austin SS",
            "Caycee SS",
            "Isela SS",
            "Pat SS",
        ]
        jnr_specialists_names = [
            "Kayla TC",
            "Kayla SS",
            "Julio TC",
            "Julio SS",
            "Sule TC",
            "Sule SS",
            "Noela TC",
            "Noela SS",
            "Molly TC",
            "Molly SS",
        ]
        setter_names = [
            "Donnah TC",
            "Liz TC",
            "Jelyn TC",
            "Jen TC",
            "Rachel TC",
            "Amanda TC",
        ]
        ops_names = ["Gussi Task", "Marl Task", "Roxan Task", "David Task"]

        return (
            pod_names,
            snr_specialist_names,
            jnr_specialists_names,
            setter_names,
            ops_names,
            df,
        )

    def create_7d_total(self):
        seven_day_total = {
            "Pods": [],
            "Snr Specialists": [],
            "Jnr Specialists": [],
            "Setters": [],
            "Ops": [],
        }

        (
            pod_names,
            snr_specialist_names,
            jnr_specialists_names,
            setter_names,
            ops_names,
            df,
        ) = self.create_dfs()

        pod_df = df.loc[pod_names]
        snr_specialist_df = df.loc[snr_specialist_names]
        jnr_specialists_df = df.loc[jnr_specialists_names]
        setter_df = df.loc[setter_names]
        ops_df = df.loc[ops_names]

        seven_day_total["Pods"] = (
            pod_df.to_frame()
            .sort_values(by="Week Total", ascending=False)
            .to_dict()["Week Total"]
        )
        seven_day_total["Snr Specialists"] = (
            snr_specialist_df.to_frame()
            .sort_values(by="Week Total", ascending=False)
            .to_dict()["Week Total"]
        )

        mydf = jnr_specialists_df.to_frame()

        counts = {
            "Kayla Score": 0,
            "Julio Score": 0,
            "Sule Score": 0,
            "Noela Score": 0,
            "Molly Score": 0,
        }
        for index in mydf.index:
            ss_count = 0
            name = index.split()[0] + " Score"
            if "SS" in index:
                ss_count += mydf.loc[index]["Week Total"] * 5
                counts[name] = ss_count

        for index in mydf.index:
            name = index.split()[0] + " Score"
            if "TC" in index:
                counts[name] = mydf.loc[index]["Week Total"] + counts[name]

        seven_day_total["Jnr Specialists"] = counts

        seven_day_total["Setters"] = (
            setter_df.to_frame()
            .sort_values(by="Week Total", ascending=False)
            .to_dict()["Week Total"]
        )
        seven_day_total["Ops"] = (
            ops_df.to_frame()
            .sort_values(by="Week Total", ascending=False)
            .to_dict()["Week Total"]
        )
        return seven_day_total, counts

    def leaderboard(self):

        seven_day_total, counts = self.create_7d_total()
        updated_df = pd.DataFrame.from_dict(seven_day_total)

        (
            pod_names,
            snr_specialist_names,
            jnr_specialists_names,
            setter_names,
            ops_names,
            df,
        ) = self.create_dfs()
        pod_lead = updated_df[updated_df.index.isin(pod_names)]["Pods"]
        snr_spec = updated_df[updated_df.index.isin(snr_specialist_names)][
            "Snr Specialists"
        ]
        jnr_spec = updated_df[updated_df.index.isin(counts.keys())]["Jnr Specialists"]
        setter = updated_df[updated_df.index.isin(setter_names)]["Setters"]
        op = updated_df[updated_df.index.isin(ops_names)]["Ops"]

        return pd.concat([pod_lead, snr_spec, jnr_spec, setter, op])
