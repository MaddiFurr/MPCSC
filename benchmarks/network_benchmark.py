import speedtest

def perform_network_speed_test():
    """Perform a network speed test and return the results."""
    print("\033[1;34m[NETWORK]\033[0m Performing network speed test...")
    system_info = {}
    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        
        system_info["Network"] = {
            "Download (Mbps)": round(st.results.download / 1000000, 2),
            "Upload (Mbps)": round(st.results.upload / 1000000, 2),
            "Ping (ms)": round(st.results.ping, 2),
        }
        print("\033[1;32m[NETWORK]\033[0m Network speed test completed!")
    except speedtest.ConfigRetrievalError:
        system_info["Network"] = {
            "Download (Mbps)": "Error",
            "Upload (Mbps)": "Error",
            "Ping (ms)": "Error",
        }
        print("\033[1;31m[NETWORK]\033[0m Error: Could not perform speed test.")

    return system_info

# Example usage
if __name__ == "__main__":
    network_info = perform_network_speed_test()
    print(network_info)