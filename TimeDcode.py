import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, available_timezones

class TimeDecoderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Decoder")
        self.root.geometry("600x750") # Taller to fit the scroll area
        self.root.resizable(True, True) # Allow resizing
        
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10, "bold"))
        style.configure("Result.TLabel", font=("Consolas", 12))
        style.configure("Result.TEntry", font=("Consolas", 12)) 

        # Main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ==========================================
        # SECTION 1: INPUTS
        # ==========================================
        ttk.Label(main_frame, text="Input Timestamp:").pack(anchor=tk.W)
        self.input_var = tk.StringVar()
        self.entry_input = ttk.Entry(main_frame, textvariable=self.input_var, width=50, font=("Consolas", 11))
        self.entry_input.pack(fill=tk.X, pady=(5, 10))

        ttk.Label(main_frame, text="Source Format (for Single Convert):").pack(anchor=tk.W)
        self.format_var = tk.StringVar(value="Unix Hex 32-bit Big Endian")
        
        # DEFINED FORMATS LIST
        self.formats = [
            "Unix Seconds (Decimal)",
            "Unix Hex 32-bit Big Endian",
            "Unix Hex 32-bit Little Endian",
            "Unix Milliseconds Hex",
            "Unix Milliseconds (Decimal)",
            "Windows FILETIME Big Endian",
            "Windows FILETIME Little Endian"
        ]
        
        self.combo_format = ttk.Combobox(main_frame, textvariable=self.format_var, values=self.formats, state="readonly")
        self.combo_format.pack(fill=tk.X, pady=(5, 10))

        # 3. Target Timezone Selection
        ttk.Label(main_frame, text="Optional Target Timezone:").pack(anchor=tk.W)
        
        # Get zones
        self.available_zones = sorted(list(available_timezones()))
        
        # SAFETY CHECK: If list is empty (common on Windows without tzdata), fallback to UTC
        if self.available_zones:
            if "America/Los_Angeles" in self.available_zones:
                default_tz = "America/Los_Angeles"
            else:
                default_tz = self.available_zones[0]
        else:
            # Fallback for Windows if tzdata is missing
            self.available_zones = ["UTC"]
            default_tz = "UTC"
            
        self.tz_var = tk.StringVar(value=default_tz)
        self.combo_tz = ttk.Combobox(main_frame, textvariable=self.tz_var, values=self.available_zones, height=10)
        self.combo_tz.pack(fill=tk.X, pady=(5, 20))

        # ==========================================
        # SECTION 2: ACTIONS
        # ==========================================
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.btn_convert = ttk.Button(btn_frame, text="CONVERT (Single)", command=self.convert_time)
        self.btn_convert.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.btn_guess = ttk.Button(btn_frame, text="GUESS / CHECK ALL", command=self.guess_all_formats)
        self.btn_guess.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        # ==========================================
        # SECTION 3: SINGLE RESULT OUTPUT
        # ==========================================
        # UTC Time display
        utc_frame = ttk.Frame(main_frame)
        utc_frame.pack(fill=tk.X, pady=2)
        ttk.Label(utc_frame, text="UTC Time:", style="Result.TLabel").pack(side=tk.LEFT)
        self.entry_utc = ttk.Entry(utc_frame, state='readonly', style="Result.TEntry", width=40)
        self.entry_utc.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.entry_utc.insert(0, "--")

        # Local Time display
        local_frame = ttk.Frame(main_frame)
        local_frame.pack(fill=tk.X, pady=2)
        ttk.Label(local_frame, text="Local Time:", style="Result.TLabel").pack(side=tk.LEFT)
        self.entry_local = ttk.Entry(local_frame, state='readonly', style="Result.TEntry", width=40)
        self.entry_local.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.entry_local.insert(0, "--")

        # Target Time display
        target_frame = ttk.Frame(main_frame)
        target_frame.pack(fill=tk.X, pady=2)
        ttk.Label(target_frame, text="Target Time:", style="Result.TLabel", foreground="#007AFF").pack(side=tk.LEFT)
        self.entry_target = ttk.Entry(target_frame, state='readonly', style="Result.TEntry", width=40)
        self.entry_target.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.entry_target.insert(0, "--")

        # ==========================================
        # SECTION 4: GUESS RESULTS LOG
        # ==========================================
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=20)
        
        ttk.Label(main_frame, text="Guess Results (Matches between 1970 - 2040):", font=("Helvetica", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        # Scrollable Text Area
        self.txt_guess = scrolledtext.ScrolledText(main_frame, height=10, state='disabled', font=("Consolas", 10))
        self.txt_guess.pack(fill=tk.BOTH, expand=True)

    def get_unix_timestamp(self, input_str, fmt):
        clean_input = input_str.strip().replace("0x", "").replace(" ", "").replace(":", "")
        if len(clean_input) % 2 != 0: clean_input = "0" + clean_input

        try:
            if fmt == "Unix Seconds (Decimal)":
                return float(int(input_str.strip()))
            elif fmt == "Unix Hex 32-bit Big Endian":
                return float(int(clean_input, 16))
            elif fmt == "Unix Hex 32-bit Little Endian":
                byte_vals = bytes.fromhex(clean_input)
                return float(int(byte_vals[::-1].hex(), 16))
            elif fmt == "Unix Milliseconds Hex":
                return int(clean_input, 16) / 1000.0
            elif fmt == "Unix Milliseconds (Decimal)":
                return int(input_str.strip()) / 1000.0
            elif fmt == "Windows FILETIME Big Endian":
                return self.windows_filetime_to_unix(int(clean_input, 16))
            elif fmt == "Windows FILETIME Little Endian":
                byte_vals = bytes.fromhex(clean_input)
                return self.windows_filetime_to_unix(int(byte_vals[::-1].hex(), 16))
            else:
                raise ValueError(f"Unknown format: {fmt}")
        except Exception:
            raise ValueError(f"Conversion failed for {fmt}")

    def windows_filetime_to_unix(self, filetime_val):
        return (filetime_val - 116444736000000000) / 10_000_000

    def convert_time(self):
        self._perform_single_conversion(self.format_var.get())

    def _perform_single_conversion(self, fmt_selection):
        input_val = self.input_var.get()
        target_tz_name = self.tz_var.get()

        if not input_val:
            messagebox.showwarning("Warning", "Please enter a timestamp value.")
            return

        try:
            epoch_seconds = self.get_unix_timestamp(input_val, fmt_selection)
            
            # Sanity Check
            if epoch_seconds > 32503680000 or epoch_seconds < -30610224000:
                 raise ValueError("Date out of bounds")

            dt_utc = datetime.fromtimestamp(epoch_seconds, timezone.utc)
            dt_local = datetime.fromtimestamp(epoch_seconds).astimezone()
            
            try:
                if target_tz_name in self.available_zones:
                    dt_target = dt_utc.astimezone(ZoneInfo(target_tz_name))
                    target_str = dt_target.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
                else:
                    target_str = "Invalid Timezone"
            except:
                target_str = "Timezone Error"

            # Update Entry widgets with time values (selectable for copy-paste)
            self.entry_utc.config(state='normal')
            self.entry_utc.delete(0, tk.END)
            self.entry_utc.insert(0, dt_utc.strftime('%Y-%m-%d %H:%M:%S.%f'))
            self.entry_utc.config(state='readonly')
            
            self.entry_local.config(state='normal')
            self.entry_local.delete(0, tk.END)
            self.entry_local.insert(0, dt_local.strftime('%Y-%m-%d %H:%M:%S.%f %Z'))
            self.entry_local.config(state='readonly')
            
            self.entry_target.config(state='normal')
            self.entry_target.delete(0, tk.END)
            self.entry_target.insert(0, target_str)
            self.entry_target.config(state='readonly')
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to decode.\n{str(e)}")

    def guess_all_formats(self):
        input_val = self.input_var.get()
        if not input_val:
            messagebox.showwarning("Warning", "Please enter a timestamp value to guess.")
            return

        # Enable text box for writing
        self.txt_guess.config(state='normal')
        self.txt_guess.delete('1.0', tk.END) # Clear previous results
        
        matches_found = 0
        
        self.txt_guess.insert(tk.END, f"Scanning input: '{input_val}'\n")
        self.txt_guess.insert(tk.END, "="*50 + "\n")

        for fmt in self.formats:
            try:
                epoch = self.get_unix_timestamp(input_val, fmt)
                
                # FILTER: Only show "Human Readable" dates (1970 - 2040)
                if 0 <= epoch <= 2208988800:
                    dt_obj = datetime.fromtimestamp(epoch, timezone.utc)
                    time_str = dt_obj.strftime('%Y-%m-%d %H:%M:%S UTC')
                    
                    # Formatting the output block
                    self.txt_guess.insert(tk.END, f"Format: {fmt}\n")
                    self.txt_guess.insert(tk.END, f"Result: {time_str}\n")
                    self.txt_guess.insert(tk.END, "-"*30 + "\n")
                    matches_found += 1
            except:
                continue

        if matches_found == 0:
            self.txt_guess.insert(tk.END, "No valid timestamps found within years 1970-2040.\n")
        
        # Disable text box to prevent user editing
        self.txt_guess.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeDecoderApp(root)
    root.mainloop()