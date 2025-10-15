import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

#load data
def load_traffic_data(file_path):
    print(f"load data from '{file_path}'...")
    try:
        column_names = [
            "Type", "sflow_agent_address", "inputPort", "outputPort", "src_MAC", "dst_MAC",
            "ethernet_type", "in_vlan", "out_vlan", "src_IP", "dst_IP", "IP_protocol",
            "ip_tos", "ip_ttl", "src_port", "dst_port", "tcp_flags",
            "packet_size", "IP_size", "sampling_rate"
        ]
        df = pd.read_csv(file_path, header=None, names=column_names)
        print("File loaded successfully!")
        return df
    except FileNotFoundError:
        print(f"\nError: '{file_path}' was not found.")
        print("make sure your Python script and the CSV file are in the same folder")
        return None

def analyse_core_metrics(df):

    #Top 5 Talkers
    top_talkers = df['src_IP'].value_counts().nlargest(5)
    print("Top 5 Talkers (Source IPs)")
    print(top_talkers)


    #Top 5 Listeners
    top_listeners = df['dst_IP'].value_counts().nlargest(5)
    print("\n Top 5 Listeners (Destination IPs)")
    print(top_listeners)

    #Top 5 Applications
    top_applications = df['dst_port'].value_counts().nlargest(5)
    print("\nTop 5 Applications (by Destination Port)")
    print(top_applications)


    #Proportion of TCP and UDP Packets
    tcp_count = df[df['IP_protocol'] == 6].shape[0]
    udp_count = df[df['IP_protocol'] == 17].shape[0]
    total_packets_in_log = len(df)
    tcp_percentage = (tcp_count / total_packets_in_log) * 100
    udp_percentage = (udp_count / total_packets_in_log) * 100

    print("\nTransport Protocol Proportion")
    print(f"TCP packets (Protocol 6): {tcp_count} ({tcp_percentage:.2f}%)")
    print(f"UDP packets (Protocol 17): {udp_count} ({udp_percentage:.2f}%)")

    #Total Estimated Traffic
    sampling_rate = df['sampling_rate'].iloc[0]
    total_ip_size_in_log = df['IP_size'].sum()
    estimated_total_traffic_bytes = total_ip_size_in_log * sampling_rate
    estimated_total_traffic_mb = estimated_total_traffic_bytes / (1024 * 1024)

    print("\nTotal Estimated Traffic")
    print(f"Total IP_size in log file: {total_ip_size_in_log} bytes")
    print(f"Sampling Rate: 1 in {sampling_rate}")
    print(f"Estimated Total Traffic: {estimated_total_traffic_mb:.2f} MB")

def analyse_and_visualise_pairs(df):
    print("\nAdditional Analysis: Top Communication Pairs")
    communication_pairs = df.groupby(['src_IP', 'dst_IP']).size().nlargest(5)
    print(communication_pairs)

    print("\nNetwork Visualisation Plot")
    try:
        G = nx.DiGraph()
        for (src, dst), count in communication_pairs.items():
            G.add_edge(src, dst, weight=count)

        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G, k=0.8, iterations=50)
        nx.draw(G, pos, with_labels=True, node_size=2500, node_color='skyblue', font_size=8, width=2, edge_color='gray')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

        plt.title("Top 5 Communication Pairs Network Graph")
        output_filename = "Network_Graph_Top5.png"
        plt.savefig(output_filename, dpi=300)
        print(f"Saved visualisation into '{output_filename}'")

    except ImportError:
        print("Skipping visualisation Please install matplotlib and 'networkx.")
        print("Run conda install matplotlib networkx")


def main():
    file_path = 'Data_2.csv'
    traffic_data = load_traffic_data(file_path)

    if traffic_data is not None:
        analyse_core_metrics(traffic_data)
        analyse_and_visualise_pairs(traffic_data)


if __name__ == "__main__":
    main()







