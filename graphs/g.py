import numpy as np
import matplotlib.pyplot as plt
import CoolProp.CoolProp as CP

# Style
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.linewidth": 1.2
})

# Brayton
bT1 = 300
bT3 = 1400
bP1 = 1e5
bPressure_ratio = 10
bmin_temp = 250
bmax_temp = 1500
intercooling = True # intercooling margin
margin = 0 # intercooling margin

# Cycle parameters
fluid = 'Water'
T_high = 500 + 273.15
#T_low = 45 + 273.15
P_low = 0.01e6
P_high = 8e6

ideal_rankine = False


# Graph config
exag_pump_temp = True
real_cycle = False
isobars = True
min_temp = 300
max_temp = 800
resolution = 1000

# Define your colors here for consistency
SATURATION_COLOR = '#1f4e79'  # Dark blue
CYCLE_COLOR = '#8b2323'       # Dark red / Maroon
ISOBAR_COLORS = ['#bbbbbb', '#aaaaaa', '#999999', '#888888', '#777777', '#666666']


def get_saturation_dome_Tv(fluid='Water', num_points=300):
    Ts = []
    Vs = []
    T_min = CP.PropsSI('Ttriple', fluid)  # Start at triple point
    T_crit = CP.PropsSI('Tcrit', fluid)
    T_vals = np.linspace(T_min, T_crit, num_points)

    for T in T_vals:
        try:
            v_l = 1 / CP.PropsSI('D', 'T', T, 'Q', 0, fluid)  # v = 1/rho
            v_v = 1 / CP.PropsSI('D', 'T', T, 'Q', 1, fluid)
            Ts.append(T)
            Vs.append(v_l)
        except:
            continue
    for T in reversed(T_vals):
        try:
            v_v = 1 / CP.PropsSI('D', 'T', T, 'Q', 1, fluid)
            Ts.append(T)
            Vs.append(v_v)
        except:
            continue
    return Vs, Ts


def plot_isobars_Tv(pressures, v_range=(1e-4, 10), T_limits=(270, 650), color_map=ISOBAR_COLORS):
    v_grid = np.logspace(np.log10(v_range[0]), np.log10(v_range[1]), resolution)
    color_map = color_map or ISOBAR_COLORS

    c = ISOBAR_COLORS[4]
    for i, p in enumerate(pressures):
        T_line, v_line = [], []
        for v in v_grid:
            try:
                rho = 1 / v
                T = CP.PropsSI('T', 'P', p, 'D', rho, fluid)
                if T_limits[0] < T < T_limits[1]:
                    T_line.append(T)
                    v_line.append(v)
            except:
                continue
        if T_line:
            plt.plot(v_line, T_line, ':', color=c, alpha=0.9)

            # Label near the line
            label = f'{p/1e5:.0f} bar' if p/1e5 == int(p/1e5) else f'{p/1e5:.1f} bar'
            idx = int(len(v_line) * 0.65) if len(v_line) > 0 else 0
            plt.text(v_line[idx], T_line[idx], label, color=c, fontsize=10,
                     va='bottom', ha='center')


def draw_Tv_diagram(filename='tv_diagram.pdf', draw_isobars=True):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Saturation dome
    v_dome, T_dome = get_saturation_dome_Tv(fluid=fluid, num_points=resolution)
    
    # Adjusting T limits to prevent the plot from being too tight
    T_min = min(T_dome)
    T_max = max(T_dome)
    T_buffer = (T_max - T_min) * 0.05  # Adding 5% buffer

    # Plot the dome with adjusted limits
    ax.plot(v_dome, T_dome, color=SATURATION_COLOR, linewidth=2, label='Saturation Dome')
    ax.fill_between(v_dome, T_dome, T_min, color=SATURATION_COLOR, alpha=0.05)

    # Critical point
    T_crit = CP.PropsSI('Tcrit', fluid)
    p_crit = CP.PropsSI('Pcrit', fluid)
    v_crit = 1 / CP.PropsSI('RHOMASS_CRITICAL', fluid)

    # Optional isobars
    if draw_isobars:
        pressures = [0.01e6, 0.1e6, 0.5e6, 2e6, 4e6, 8e6, 22.09e6, 30e6, 60e6]  # Pascals
        plot_isobars_Tv(pressures, v_range=(6e-4, 3e2), T_limits=(T_min - T_buffer, max_temp))

    ax.plot(v_crit, T_crit, 'ko', label='Ponto Crítico')

    # Axes settings
    ax.set_xlabel("Volume específico $v$ [$m^3/kg$]")
    ax.set_ylabel("Temperatura $T$ [K]")
    ax.set_xscale('log')  # Volume varies a lot, log scale looks better
    ax.set_xlim(left=6e-4, right=3e2)
    ax.set_ylim(bottom=T_min - T_buffer, top=max_temp)  # Adjusting y-limits with padding
    ax.spines['left'].set_position(('data', 6e-4))
    ax.spines['bottom'].set_position(('data', T_min))
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.legend().set_visible(False)
    ax.set_aspect('auto')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()



def get_saturation_dome(fluid='Water', num_points=300):
    Ts = []
    Ss = []
    T_min = CP.PropsSI('Tmin', fluid)
    T_crit = CP.PropsSI('Tcrit', fluid)
    T_vals = [T_min + i * (T_crit - T_min) / (num_points - 1) for i in range(num_points)]
    for T in T_vals:
        try:
            s_l = CP.PropsSI('S', 'T', T, 'Q', 0, fluid) / 1000
            s_v = CP.PropsSI('S', 'T', T, 'Q', 1, fluid) / 1000
            Ts.append(T)
            Ss.append(s_l)
        except:
            continue
    for T in reversed(T_vals):
        try:
            s_v = CP.PropsSI('S', 'T', T, 'Q', 1, fluid) / 1000
            Ts.append(T)
            Ss.append(s_v)
        except:
            continue
    return Ss, Ts


def plot_isobars(pressures, s_range=(0.5, 9), T_limits=(min_temp, max_temp), color_map=ISOBAR_COLORS):
    s_grid = np.linspace(*s_range, resolution)
    color_map = color_map or ISOBAR_COLORS# plt.cm.viridis(np.linspace(0.2, 0.8, len(pressures)))

    i = -1
    c = ISOBAR_COLORS[4]
    for p in (pressures):
        i += 1
        T_line, s_line = [], []
        for s in s_grid:
            try:
                T = CP.PropsSI('T','P',p,'S',s*1000,fluid)
                if T_limits[0] < T < T_limits[1]:
                    T_line.append(T)
                    s_line.append(s)
            except:
                continue
        if T_line:
            plt.plot(s_line, T_line, ':', color=c, alpha=0.9)

            # Add text near the top of the line (you can adjust the position here)
            label = f'{p/1e5:.0f} bar' if p / 1e5 == int(p/ 1e5) else f'{p/1e5:.1f} bar'

            # if i == 2:
            #     text_position = (s_line[int(len(s_line)*(0.78-float(float(i)/80)) )], T_line[int(len(T_line)*(0.78-float(float(i)/80)) )])  # Pick a point near the top
            # elif i == 1:
            #     text_position = (s_line[int(len(s_line)*(0.83) )], T_line[int(len(T_line)*(0.83) )])  # Pick a point near the top
            # elif i < 3:
            if i == 2:
                text_position = (s_line[int(len(s_line)*(0.88) )], T_line[int(len(T_line)*(0.88) )])  # Pick a point near the top
            elif i == 1:
                text_position = (s_line[int(len(s_line)*(0.75) )], T_line[int(len(T_line)*(0.75) )])  # Pick a point near the top
            elif i == 0:
                text_position = (s_line[int(len(s_line)*(0.8) )], T_line[int(len(T_line)*(0.8) )])  # Pick a point near the top
            else:
                text_position = (s_line[int(len(s_line)*(0.82-float(float(i)/60)) )], T_line[int(len(T_line)*(0.82-float(float(i)/60)) )])  # Pick a point near the top
            plt.text(text_position[0], text_position[1], label, color=c, fontsize=10, va='bottom', ha='center')






################################## BRAYTON ##################################

def brayton_cycle(T1=300, T3=1400, P1=1e5, gamma=1.4, R=0.287, 
                  eta_c=0.8, eta_t=0.88, label='Air', intercooling=False):
    """
    Brayton cycle with optional intercooling and isentropic efficiencies.
    
    Returns:
        ideal_points: List of (s [kJ/kg·K], T [K]) for ideal cycle
        real_points: List of (s [kJ/kg·K], T [K]) for real cycle
    """
    ideal = []
    real = []

    # Compressor outlet pressure
    P2 = P1 * bPressure_ratio

    if intercooling:
        # --- Intercooling option ---
        P_opt = np.sqrt(P1 * P2)

        # --- State 1 (Inlet) ---
        s1 = CP.PropsSI('S', 'T', T1, 'P', P1, label) / 1000
        h1 = CP.PropsSI('H', 'T', T1, 'P', P1, label) / 1000

        # --- Ideal path ---
        # Isentropic compression to P_opt
        T2s = CP.PropsSI('T', 'P', P_opt, 'S', s1 * 1000, label)
        s2s = s1
        h2s = CP.PropsSI('H', 'T', T2s, 'P', P_opt, label) / 1000

        # Isobaric cooling to T1
        s2 = CP.PropsSI('S', 'P', P_opt, 'T', T1, label) / 1000
        h2 = CP.PropsSI('H', 'P', P_opt, 'T', T1, label) / 1000

        # Isentropic compression to P2
        T3s = CP.PropsSI('T', 'P', P2, 'S', s2 * 1000, label)
        s3s = s2
        h3s = CP.PropsSI('H', 'T', T3s, 'P', P2, label) / 1000

        ideal = [
            (s1, T1),     # 1
            (s2s, T2s),   # 2s (after 1st isentropic compression)
            (s2, T1),     # 2 (after cooling to T1)
            (s3s, T3s),   # 3s (after 2nd isentropic compression)
        ]

        # Heat addition (3 → 4)
        h4 = CP.PropsSI('H', 'T', T3, 'P', P2, label) / 1000
        s4 = CP.PropsSI('S', 'T', T3, 'P', P2, label) / 1000
        ideal.append((s4, T3))

        # Isentropic expansion to P1
        T5s = CP.PropsSI('T', 'P', P1, 'S', s4 * 1000, label)
        s5s = s4
        ideal.append((s5s, T5s))

        if real_cycle:
            # --- Real path ---
            # Real 1st compression
            h2r = h1 + (h2s - h1) / eta_c
            T2r = CP.PropsSI('T', 'P', P_opt, 'H', h2r * 1000, label)
            s2r = CP.PropsSI('S', 'T', T2r, 'P', P_opt, label) / 1000

            # Cool to T1 (same as ideal)
            s3r = s2
            h3r = h2  # Same enthalpy at T1

            # Real 2nd compression
            h4r = h3r + (h3s - h3r) / eta_c
            T4r = CP.PropsSI('T', 'P', P2, 'H', h4r * 1000, label)
            s4r = CP.PropsSI('S', 'T', T4r, 'P', P2, label) / 1000

            # Heat addition to T3
            h5r = CP.PropsSI('H', 'T', T3, 'P', P2, label) / 1000
            s5r = CP.PropsSI('S', 'T', T3, 'P', P2, label) / 1000

            # Real expansion
            h6s = CP.PropsSI('H', 'T', T5s, 'P', P1, label) / 1000
            h6r = h5r - eta_t * (h5r - h6s)
            T6r = CP.PropsSI('T', 'P', P1, 'H', h6r * 1000, label)
            s6r = CP.PropsSI('S', 'T', T6r, 'P', P1, label) / 1000

            real = [
                (s1, T1), (s2r, T2r), (s2, T1), (s4r, T4r), (s5r, T3), (s6r, T6r)
            ]

    else:
        # --- No intercooling ---
        s1 = CP.PropsSI('S', 'T', T1, 'P', P1, label) / 1000
        h1 = CP.PropsSI('H', 'T', T1, 'P', P1, label) / 1000

        s2s = s1
        T2s = CP.PropsSI('T', 'P', P2, 'S', s2s * 1000, label)
        h2s = CP.PropsSI('H', 'T', T2s, 'P', P2, label) / 1000

        h2 = h1 + (h2s - h1) / eta_c
        T2 = CP.PropsSI('T', 'P', P2, 'H', h2 * 1000, label)
        s2 = CP.PropsSI('S', 'T', T2, 'P', P2, label) / 1000

        h3 = CP.PropsSI('H', 'T', T3, 'P', P2, label) / 1000
        s3 = CP.PropsSI('S', 'T', T3, 'P', P2, label) / 1000

        T4s = CP.PropsSI('T', 'P', P1, 'S', s3 * 1000, label)
        h4s = CP.PropsSI('H', 'T', T4s, 'P', P1, label) / 1000

        h4 = h3 - eta_t * (h3 - h4s)
        T4 = CP.PropsSI('T', 'P', P1, 'H', h4 * 1000, label)
        s4 = CP.PropsSI('S', 'T', T4, 'P', P1, label) / 1000

        ideal = [(s1, T1), (s2s, T2s), (s3, T3), (s3, T4s)]
        if real_cycle:
            real = [(s1, T1), (s2, T2), (s3, T3), (s4, T4)]

    return ideal, real if real_cycle else None



def draw_brayton_isobar(s_start, s_end, pressure, label='Air', color='gray', style=':', ax=None):
    if ax is None:
        return

    s_vals = np.linspace(s_start, s_end, 100)
    T_vals = []

    for s in s_vals:
        try:
            T = CP.PropsSI('T', 'P', pressure, 'S', s * 1000, label)
            T_vals.append(T)
        except:
            T_vals.append(np.nan)  # Skip invalid states

    ax.plot(s_vals, T_vals, linestyle=style, color=color, linewidth=2)


def get_isentropic_point(s1, T1, P1, P2, gamma=1.4):
    """
    Calculate the entropy-preserving point for ideal gas: s = const
    Returns (s2, T2)
    """
    T2 = T1 * (P2 / P1) ** ((gamma - 1) / gamma)
    s2 = s1  # Isentropic → entropy doesn't change
    return s2, T2

def get_isobaric_point(s1, T1, P, T2):
    """
    Calculate the point at constant pressure from T1 to T2.
    Returns (s2, T2), approximating entropy change for an ideal gas.
    """
    cp = 1005  # J/(kg·K) for air
    s2 = s1 + cp * np.log(T2 / T1) / 1000  # entropy in kJ/kg·K
    return s2, T2


def draw_cycle_brayton(ideal, real=None, label_points=True, ax=None, min_temp=300, max_temp=1800, intercooling=False):
    if not ax:
        return

    def connect(p1, p2, style='-', color=CYCLE_COLOR):
        s_vals = [p1[0], p2[0]]
        T_vals = [p1[1], p2[1]]
        ax.plot(s_vals, T_vals, style, color=color, linewidth=2)

    isobar_color = 'gray'
    P1 = bP1
    P2 = bP1 * bPressure_ratio
    offset = 0.5
    P_opt = np.sqrt(P1 * P2)

    s_min = min(ideal[i][0] for i in range(len(ideal)))
    if real:
        s_max = max(real[i][0] for i in range(len(real)))
    else:
        s_max = max(ideal[i][0] for i in range(len(ideal)))

    # --- Draw Isobars ---
    draw_brayton_isobar(s_min - offset, s_max + offset, P2, label='Air', color=isobar_color, style=':', ax=ax)  # 2 → 3
    draw_brayton_isobar(s_min - offset, s_max + offset, P1, label='Air', color=isobar_color, style=':', ax=ax)  # 4 → 1
    if intercooling:
        draw_brayton_isobar(s_min - offset, s_max + offset, P_opt, label='Air', color=isobar_color, style=':', ax=ax)  # 4 → 1

    secondtime = False
    for points in (ideal, real):
        if not points:
            continue
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i + 1]
            line_style = '-' if (secondtime or not real) else '--'

            if intercooling:
                if i == 1:
                    draw_brayton_isobar(p1[0], p2[0], P_opt, label='Air', color=CYCLE_COLOR, style=line_style, ax=ax)
                elif i == 3:
                    draw_brayton_isobar(p1[0], p2[0], P2, label='Air', color=CYCLE_COLOR, style=line_style, ax=ax)
                else:
                    connect(p1, p2, style=line_style)
            else:
                if i == 1:
                    draw_brayton_isobar(p1[0], p2[0], P2, label='Air', color=CYCLE_COLOR, style=line_style, ax=ax)
                else:
                    connect(p1, p2, style=line_style)
        secondtime = True

    # --- Label Points ---
    if label_points:
        for i, (s, T) in enumerate(ideal):
            if min_temp <= T <= max_temp:
                ax.plot(s, T, 'ko')
                offset_x = -0.08 if (i <= 3) else 0.05
                offset_y = 5
                if not real:
                    if intercooling:
                        if (i == 1):
                            ax.text(s + offset_x, T + offset_y, f'c', fontsize=11, fontweight="bold")
                        elif (i == 2):
                            ax.text(s + offset_x, T + offset_y, f'd', fontsize=11, fontweight="bold")
                        elif (i == 0):
                            ax.text(s + offset_x, T + offset_y, f'1', fontsize=11, fontweight="bold")
                        else:
                            ax.text(s + offset_x, T + offset_y, f'{i-1}', fontsize=11, fontweight="bold")
                    else:
                        ax.text(s + offset_x, T + offset_y, f'{i+1}', fontsize=11, fontweight="bold")
                else:
                    if (i == 1 or i == 3):
                        ax.text(s + offset_x, T + offset_y, f'{i+1}s', fontsize=11, fontweight="bold")


        if real:
            for i, (s, T) in enumerate(real):
                if min_temp <= T <= max_temp:
                    ax.plot(s, T, 'ko')
                    offset_x = -0.05 if (i <= 3) else 0.05
                    offset_y = 5 if i != 0 else -5
                    ax.text(s + offset_x, T + offset_y, f'{i+1}', fontsize=11, fontweight="bold")




def draw_ts_cycle_brayton(points_ideal, label_points=True, filename='cycle_ts_brayton.pdf',
                          min_temp=300, max_temp=1800, points_real=None, fluid='Air', intercooling=False):
    if not points_ideal:
        print("Error: No valid points generated for the cycle.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    # --- Draw Cycle ---
    draw_cycle_brayton(ideal=points_ideal, real=points_real, label_points=label_points, ax=ax,
                       min_temp=min_temp, max_temp=max_temp, intercooling=intercooling)

    # --- Cut the X-Axis Range Based on Entropy Values (Without Adjusting Graph) ---

    s_min = min(points_ideal[i][0] for i in range(len(points_ideal)))
    if points_real:
        s_max = max(points_real[i][0] for i in range(len(points_real)))
    else:
        s_max = max(points_ideal[i][0] for i in range(len(points_ideal)))
    offset = 0.2 * (s_max - s_min)  # 10% offset from min and max entropy
    ax.set_xlim(left=s_min - offset, right=s_max + offset)  # Limit the x-axis without changing the graph

    # --- Axes Formatting ---
    ax.set_xlabel("Entropia $s$ [kJ/kg·K]")
    ax.set_ylabel("Temperatura $T$ [K]")
    ax.set_ylim(bottom=min_temp, top=max_temp)

    # Positioning for Entropy (X-axis)
    ax.spines['left'].set_position(('data', s_min - offset))  # Entropy axis starts at 0, if desired
    ax.spines['bottom'].set_position(('data', min_temp))  # Temperature axis starts at the minimum temperature value
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    # --- Save or Show the Plot ---
    ax.legend().set_visible(False)
    ax.set_aspect('auto')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()



######################### RANKINE #########################

def rankine_cycle(P_high=8e6, P_low=0.01e6, T_high=773.15, exag_pump_temp=True, 
                  show_real_cycle=False, eta_pump=0.08, eta_turbine=0.85):
    """
    Generates T-s state points for a simple Rankine cycle using water.
    Returns list of (s [kJ/kg·K], T [K]) tuples for plotting.
    """
    # STATE 1: Saturated liquid at condenser pressure
    h1 = CP.PropsSI('H', 'P', P_low, 'Q', 0, fluid)
    s1 = CP.PropsSI('S', 'P', P_low, 'Q', 0, fluid) / 1000
    T1 = CP.PropsSI('T', 'P', P_low, 'Q', 0, fluid)

    # STATE 2: After isentropic pumping to P_high (s2 = s1)
    s2s = s1
    h2s = CP.PropsSI('H', 'P', P_high, 'S', s2s * 1000, fluid)
    T2s = CP.PropsSI('T', 'P', P_high, 'S', s2s * 1000, fluid)
    
    if exag_pump_temp:
        T2s = T1 + 0.1 * (T_high - T1)  # exaggerate pump rise to 15% of boiler range

    # Real Pump
    h2 = h1 + (h2s - h1) / eta_pump
    T2 = CP.PropsSI('T', 'P', P_high, 'H', h2, fluid)
    s2 = CP.PropsSI('S', 'P', P_high, 'H', h2, fluid) / 1000

    if exag_pump_temp:
        T_sat = CP.PropsSI('T', 'P', P_high, 'Q', 0, fluid)
        s_f = CP.PropsSI('S', 'P', P_high, 'Q', 0, fluid) / 1000

        b = T2s - (T_sat - T2s)/(s_f - s2s)  * s2s
        T2 = (T_sat - T2s)/(s_f - s2s) * s2 + b

    # STATE 3: Superheated vapor at T_high and P_high
    if ideal_rankine:
        h3 = CP.PropsSI('H', 'P', P_high, 'Q', 1, fluid)      # [J/kg]
        s3 = CP.PropsSI('S', 'P', P_high, 'Q', 1, fluid) / 1000  # [kJ/kg·K]
        T3 = CP.PropsSI('T', 'P', P_high, 'Q', 1, fluid)      # [K]
    else:
        h3 = CP.PropsSI('H', 'P', P_high, 'T', T_high, fluid)
        s3 = CP.PropsSI('S', 'P', P_high, 'T', T_high, fluid) / 1000
        T3 = T_high

    # STATE 4: Isentropic expansion to P_low (s4 = s3)
    s4s = s3
    h4s = CP.PropsSI('H', 'P', P_low, 'S', s4s * 1000, fluid)
    T4s = CP.PropsSI('T', 'P', P_low, 'S', s4s * 1000, fluid)

    print( CP.PropsSI('Q', 'P', P_low, 'S', s4s * 1000, fluid))

    # Real Turbine
    h4 = h3 - eta_turbine * (h3 - h4s)
    T4 = CP.PropsSI('T', 'P', P_low, 'H', h4, fluid)
    s4 = CP.PropsSI('S', 'P', P_low, 'H', h4, fluid) / 1000

    ideal_points = [(s1, T1), (s2s, T2s), (s3, T3), (s4s, T4s)]
    if show_real_cycle:
        real_points = [(s1, T1), (s2, T2), (s3, T3), (s4, T4)]
        return ideal_points, real_points
    else:
        return ideal_points, None
    

def get_cycle_segments(points, P_high, P_low, exag_pump_temp=False):
    s1, T1 = points[0]
    s2, T2 = points[1]
    s3, T3 = points[2]
    s4, T4 = points[3]

    # Saturation temperature at P_high
    T_sat = CP.PropsSI('T', 'P', P_high, 'Q', 0, fluid)
    s_f = CP.PropsSI('S', 'P', P_high, 'Q', 0, fluid) / 1000

    segments = []

    # 1 → 2:
    segments.append(([s1, s2], [T1, T2]))

    # 2 → 3: Exaggerated process to superheated state
    if exag_pump_temp:
        segments.append(([s2, s_f], [T2, T_sat]))

        s_vals = np.linspace(s_f, s3, resolution)
        T_vals = []
        for s in s_vals:
            try:
                T = CP.PropsSI('T', 'P', P_high, 'S', s * 1000, fluid)
                T_vals.append(T)
            except:
                T_vals.append(np.nan)

        segments.append((s_vals, T_vals))
    else:
        # Normal process line from 2 to 3 (isobaric heating from liquid to superheated)
        s_vals = np.linspace(s2, s3, resolution)
        T_vals = []
        for s in s_vals:
            try:
                T = CP.PropsSI('T', 'P', P_high, 'S', s * 1000, fluid)
                T_vals.append(T)
            except:
                T_vals.append(np.nan)
        segments.append((s_vals, T_vals))

    # 3 → 4: Isentropic expansion (vertical line from s3 to s4)
    segments.append(([s3, s4], [T3, T4]))

    # 4 → 1: Isobaric condensation (from s4 back to s1)
    s_vals = np.linspace(s4, s1, resolution)
    T_vals = []
    for s in s_vals:
        try:
            T = CP.PropsSI('T', 'P', P_low, 'S', s * 1000, fluid)
            T_vals.append(T)
        except:
            T_vals.append(np.nan)
    segments.append((s_vals, T_vals))

    return segments


def draw_cycle(ideal, real=None, label_points=True, ax=None):
    if not ax:
        return

    segments = get_cycle_segments(ideal, P_high=P_high, P_low=P_low, exag_pump_temp=exag_pump_temp)

    # Plotting loop
    for segment in segments:
        if isinstance(segment, dict):  # This is a dashed line for exaggeration
            ax.plot(segment["s"], segment["T"], linestyle='--', color=CYCLE_COLOR, linewidth=2)
        else:
            s_seg, T_seg = segment
            if real:
                ax.plot(s_seg, T_seg, '--', color=CYCLE_COLOR, linewidth=2)
            else:
                ax.plot(s_seg, T_seg, '-', color=CYCLE_COLOR, linewidth=2)

    if real:
        # Cycle segments
        segments = get_cycle_segments(real, P_high=P_high, P_low=P_low, exag_pump_temp=exag_pump_temp)

        # Plotting loop
        for segment in segments:
            if isinstance(segment, dict):  # This is a dashed line for exaggeration
                ax.plot(segment["s"], segment["T"], linestyle='--', color=CYCLE_COLOR, linewidth=2)
            else:
                s_seg, T_seg = segment
                ax.plot(s_seg, T_seg, '-', color=CYCLE_COLOR, linewidth=2)

    # Plot and label state points
    if label_points:
        for i, (s, T) in enumerate(ideal):
            if min_temp <= T <= max_temp:
                ax.plot(s, T, 'ko')  # Black point marker
                offset_x = -0.4 if i == 1 else 0.1
                offset_y = 5 if i != 0 else -15
                if not real:
                    ax.text(s + offset_x, T + offset_y, f'{i+1}', fontsize=11, fontweight="bold")
                else:
                    if (i == 1 or i == 3):
                        ax.text(s + offset_x, T + offset_y, f'{i+1}s', fontsize=11, fontweight="bold")

        # Plot and label real state points
        if real:
            for i, (s, T) in enumerate(real):
                if min_temp <= T <= max_temp:
                    ax.plot(s, T, 'ko')  # Black point marker
                    offset_x = -0.2 if i == 1 else 0.1
                    offset_y = 5 if i != 0 else -15
                    ax.text(s + offset_x, T + offset_y, f'{i+1}', fontsize=11, fontweight="bold")

    return


def draw_ts_cycle(points_ideal, label_points=True, filename='cycle_ts.pdf',
                  draw_isobars=False, min_temp=300, max_temp=800, points_real=None):
    if not points_ideal:
        print("Error: No valid points generated for the cycle.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    # Saturation dome
    s_dome, T_dome = get_saturation_dome(fluid=fluid, num_points=resolution)
    s_dome = [s for s, T in zip(s_dome, T_dome) if min_temp <= T <= max_temp]
    T_dome = [T for T in T_dome if min_temp <= T <= max_temp]
    ax.plot(s_dome, T_dome, color=SATURATION_COLOR, linewidth=2, label='Saturation Dome')
    ax.fill_between(s_dome, T_dome, min_temp, color=SATURATION_COLOR, alpha=0.05)

    # Optional isobars
    if draw_isobars:
        pressures = [0.01e6, 0.1e6, 0.5e6, 2e6, 4e6, 8e6]
        plot_isobars(pressures, T_limits=(min_temp, max_temp))

    # Draw cycles
    draw_cycle(ideal=points_ideal, real=points_real, label_points=label_points, ax=ax)

    # Axes settings
    ax.set_xlabel("Entropia $s$ [kJ/kg·K]")
    ax.set_ylabel("Temperatura $T$ [K]")
    ax.set_xlim(left=0, right=max(s_dome))#max(s1, s2, s3, s4) + 1)
    ax.set_ylim(bottom=min_temp, top=max_temp)
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', min_temp))
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.legend().set_visible(False)
    ax.set_aspect('auto')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


######################### CARNOT #########################

def carnot_cycle(T_high=400, T_low=303.15):
    """
    Carnot cycle in the saturated dome: s2 = sat. liquid @ T_high, s3 = sat. vapor @ T_high
    Returns list of (s [kJ/kg·K], T [K]) tuples for plotting.
    """
    
    # State 2: Saturated liquid at T_high
    s2 = CP.PropsSI('S', 'T', T_high, 'Q', 0, fluid) / 1000
    T2 = T_high

    # State 3: Saturated vapor at T_high
    s3 = CP.PropsSI('S', 'T', T_high, 'Q', 1, fluid) / 1000
    T3 = T_high

    # State 4: Isentropic expansion to T_low (s = s3)
    s4 = s3
    T4 = T_low
    # Ensure state exists (must be inside saturation dome or superheated)
    try:
        CP.PropsSI('H', 'T', T4, 'S', s4 * 1000, fluid)
    except:
        raise ValueError("State 4 is not reachable for this fluid at given T_low.")

    # State 1: Isentropic compression to T_high (s = s2)
    s1 = s2
    T1 = T_low
    try:
        CP.PropsSI('H', 'T', T1, 'S', s1 * 1000, fluid)
    except:
        raise ValueError("State 1 is not reachable for this fluid at given T_low.")

    return [(s1, T1), (s2, T2), (s3, T3), (s4, T4)]


def draw_cycle_carnot(ideal, real=None, label_points=True, ax=None, min_temp=300, max_temp=800):
    if not ax:
        return

    # Draw ideal Carnot cycle
    for i in range(len(ideal)):
        p1 = ideal[i]
        p2 = ideal[(i + 1) % len(ideal)]
        if real:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], '--', color=CYCLE_COLOR, linewidth=2)
        else:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], '-', color=CYCLE_COLOR, linewidth=2)

    # Draw real Carnot cycle
    if real:
        for i in range(len(real)):
            p1 = real[i]
            p2 = real[(i + 1) % len(real)]
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], '-', color=CYCLE_COLOR, linewidth=2)

    # Label points
    if label_points:
        for i, (s, T) in enumerate(ideal):
            if min_temp <= T <= max_temp:
                ax.plot(s, T, 'ko')
                offset_x = 0.2
                offset_y = 5
                label = f'{i+1}s' if real and i in (1, 3) else f'{i}'
                if i == 0:
                    label = 4
                ax.text(s + offset_x, T + offset_y, label, fontsize=11, fontweight="bold")

        if real:
            for i, (s, T) in enumerate(real):
                if min_temp <= T <= max_temp:
                    ax.plot(s, T, 'ko')
                    offset_x = -0.2 if i == 1 else 0.1
                    offset_y = 5
                    ax.text(s + offset_x, T + offset_y, f'{i+1}', fontsize=11, fontweight="bold")


def draw_ts_cycle_carnot(points_ideal, label_points=True, filename='cycle_ts_carnot.pdf',
                         draw_isobars=False, min_temp=300, max_temp=800, points_real=None):
    if not points_ideal:
        print("Error: No valid points generated for the cycle.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))

    # Saturation dome
    s_dome, T_dome = get_saturation_dome(num_points=resolution)
    s_dome = [s for s, T in zip(s_dome, T_dome) if min_temp <= T <= max_temp]
    T_dome = [T for T in T_dome if min_temp <= T <= max_temp]
    ax.plot(s_dome, T_dome, color=SATURATION_COLOR, linewidth=2, label='Saturation Dome')
    ax.fill_between(s_dome, T_dome, min_temp, color=SATURATION_COLOR, alpha=0.05)

    # Optional isobars
    if draw_isobars:
        pressures = [0.01e6, 0.1e6, 0.5e6, 2e6, 4e6, 8e6]
        plot_isobars(pressures, T_limits=(min_temp, max_temp))

    # Draw cycle
    draw_cycle_carnot(ideal=points_ideal, real=points_real, label_points=label_points, ax=ax,
                      min_temp=min_temp, max_temp=max_temp)

    # Axes settings
    ax.set_xlabel("Entropia $s$ [kJ/kg·K]")
    ax.set_ylabel("Temperatura $T$ [K]")
    ax.set_xlim(left=0, right=max(s_dome))
    ax.set_ylim(bottom=min_temp, top=max_temp)
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', min_temp))
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.legend().set_visible(False)
    ax.set_aspect('auto')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()





def draw_pv_cycle(points, label_points=True, filename='diesel_pv.pdf', min_P=1e5, max_P=2e7):
    fig, ax = plt.subplots(figsize=(6, 6))  # Square aspect ratio

    # Plot the cycle in P-v space
    v_vals = [pt[0] for pt in points] + [points[0][0]]
    P_vals = [pt[1] for pt in points] + [points[0][1]]

    # Filter based on min and max pressure values
    v_vals = [v for v, P in zip(v_vals, P_vals) if P >= min_P and P <= max_P]
    P_vals = [P for P in P_vals if P >= min_P and P <= max_P]
    
    ax.plot(v_vals, P_vals, 'r-o', linewidth=2)

    # Optionally label points
    if label_points:
        for i, (v, P) in enumerate(zip(v_vals, P_vals)):
            ax.text(v * 1.02, P * 1.05, f'{i+1}', fontsize=12)


    # Clean up axes: set labels and cross at zero
    ax.set_xlabel("Volume $v$ [m³/kg]")
    ax.set_ylabel("Pressure $P$ [Pa]")
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(left=min(v_vals) * 0.8, right=max(v_vals) * 1.2)
    ax.set_ylim(bottom=min(P_vals) * 0.8, top=max(P_vals) * 1.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    # Remove the legend
    ax.legend().set_visible(False)

    # Tidy up the grid and appearance
    ax.grid(False)  # Remove grid lines
    ax.set_aspect('auto')  # Ensure square-like appearance
    plt.tight_layout()

    # Save the figure
    plt.savefig(filename)
    plt.show()






def diesel_cycle(v1=1, r=15, rc=2, P1=1e5, T1=300, gamma=1.4):
    """
    Ideal Diesel cycle on a P-v diagram.
    r = compression ratio
    rc = cutoff ratio
    """
    R = 287
    v2 = v1 / r
    v3 = v2 * rc
    v4 = v1

    T2 = T1 * (r)**(gamma - 1)
    P2 = P1 * (r)**gamma

    T3 = T2 * rc
    P3 = P2 * rc**(gamma / (rc - 1))  # approximate

    T4 = T3 * (v3 / v4)**(1 - gamma)
    P4 = P3 * (v3 / v4)**(-gamma)

    v = [v1, v2, v3, v4]
    P = [P1, P2, P3, P4]

    return list(zip(v, P))




# Run
if __name__ == '__main__':
    ideal, real = rankine_cycle(T_high=T_high, P_low=P_low, P_high=P_high, exag_pump_temp=exag_pump_temp, show_real_cycle=real_cycle)
    draw_ts_cycle(points_ideal=ideal, points_real=real, min_temp=min_temp, max_temp=max_temp, draw_isobars=isobars, filename='rankine_ts.pdf')

    # t_points = carnot_cycle(523.5, 319)
    # draw_ts_cycle_carnot(points_ideal=t_points, min_temp=min_temp, max_temp=max_temp, draw_isobars=isobars, filename='carnot_ts.pdf')

    # ideal_brayton, real_brayton = brayton_cycle(T1=bT1, T3=bT3, P1=bP1, gamma=1.4, R=0.287, intercooling=intercooling)
    # draw_ts_cycle_brayton(points_ideal=ideal_brayton, points_real=real_brayton, filename="brayton_cycle.pdf", fluid="Air", min_temp=bmin_temp, max_temp=bmax_temp, intercooling=intercooling)

    # draw_Tv_diagram(draw_isobars=True)