import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import seaborn as sns

data = pd.read_csv('data/Churn_Modelling.csv',sep=";")
# One-Hot Encoding untuk kolom kategorik
data_encoded = pd.get_dummies(data, columns=['Gender', 'HasCrCard', 'IsActiveMember'], drop_first=False)

X = data_encoded.drop(columns=['Exited'])  # Fitur
y = data_encoded['Exited']  # Label
# Simpan urutan kolom yang dihasilkan dari encoding untuk penggunaan nanti
columns_after_encoding = X.columns

# Scaling fitur
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=columns_after_encoding)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)

# Oversampling menggunakan SMOTE untuk menyeimbangkan data training
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Mengubah data training dan testing menjadi tensor PyTorch
X_train_tensor = torch.tensor(X_train_smote.values, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train_smote.values, dtype=torch.float32).unsqueeze(1)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).unsqueeze(1)
# Membuat model ANN
class ANN_Model(nn.Module):
    def __init__(self):
        super(ANN_Model, self).__init__()
        self.fc1 = nn.Linear(X_train_tensor.shape[1], 8)  # Input layer sesuai dengan jumlah kolom numerik
        self.fc2 = nn.Linear(8, 16)  # Hidden layer 1
        self.fc3 = nn.Linear(16, 8)  # Hidden layer 2
        self.fc4 = nn.Linear(8, 1)  # Output layer (1 neuron untuk prediksi binary)

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # Aktivasi relu di hidden layer 1
        x = torch.relu(self.fc2(x))  # Aktivasi relu di hidden layer 2
        x = torch.relu(self.fc3(x))  # Aktivasi relu di hidden layer 3
        x = torch.sigmoid(self.fc4(x))  # Aktivasi sigmoid di output layer untuk prediksi binary
        return x

# Inisialisasi model, loss function, dan optimizer
model = ANN_Model()
criterion = nn.BCELoss()  # Menggunakan Binary Cross-Entropy Loss untuk masalah klasifikasi biner
optimizer = optim.Adam(model.parameters(), lr=0.01)  # Menggunakan Adam optimizer

# Melatih model
epochs = 1500  # Jumlah epoch
for epoch in range(epochs):
    model.train()  # Set model ke mode training
    optimizer.zero_grad()  # Reset gradien

    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)

    # Backward pass dan optimisasi
    loss.backward()  # Menghitung gradien
    optimizer.step()  # Update parameter

# Inisialisasi model, loss function, dan optimizer
model = ANN_Model()
criterion = nn.MSELoss(reduction='mean') # Binary Cross-Entropy Loss untuk masalah klasifikasi biner
optimizer = optim.Adam(model.parameters(), lr=0.01)  # Menggunakan Adam optimizer
# Melatih model
epochs = 1500  # Jumlah epoch

for epoch in range(epochs):
    model.train()  # Set model ke mode training
    optimizer.zero_grad()  # Reset gradien

    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)

    # Backward pass dan optimisasi
    loss.backward()  # Menghitung gradien
    optimizer.step()  # Update parameter

    # Print loss setiap 100 epoch
    if epoch % 100 == 0:
        print(f"Epoch: {epoch} && Loss: {loss.item():.4f}")

# Fungsi untuk preprocessing data baru
def preprocess_input_data(input_data, columns_after_encoding):
    # One-Hot Encoding pada data input
    input_encoded = pd.get_dummies(input_data, columns=['Gender', 'HasCrCard', 'IsActiveMember'], drop_first=False)

    # Align kolom input dengan kolom training menggunakan reindex
    input_encoded = input_encoded.reindex(columns=columns_after_encoding, fill_value=0)

    # Scaling data
    input_scaled = scaler.transform(input_encoded)
    return input_scaled

st.set_page_config(
    page_title="BANK CUSTOMER CHURNAnalysis",
    page_icon="📊",
)

st.markdown("""
    <style>
    .title {
        font-size: 30px;
        color: #000000;
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin-bottom: 20px;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    <h1 class="title">DASHBOARD BANK CUSTOMER CHURN</h1>
    """, unsafe_allow_html=True)

# Sidebar with option menu
with st.sidebar:
    selected = option_menu(
        menu_title="DASHBOARD",
        options=["Home", "Visualization", "Prediction"], 
    )

# CSS for gradient background
gradient_style = """
    <style>
    .reportview-container {
        background: linear-gradient(to right, #76c893, #ffd700);
        height: 100vh;
        color: white;
    }
    .sidebar .sidebar-content {
        background: #f0f0f0;  /* Optional: change sidebar background */
    }
    </style>
"""
st.markdown(gradient_style, unsafe_allow_html=True)

# If the user selects Home
# Home Page Content
if selected == "Home":
    st.markdown("""
        <style>
        .shimmer {
            font-size: 40px;  /* Membuat teks lebih besar */
            font-weight: 900;  /* Membuat teks lebih tebal */
            text-align: center;
            color: black;  /* Warna teks hitam solid */
            position: relative;
        }

        .shimmer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.5) 50%, rgba(255,255,255,0) 100%);
            background-size: 200% 200%;
            animation: shimmer 4s infinite;
        }

        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        </style>

        <h1 class='shimmer'>Welcome to the Dashboard</h1>

        <marquee behavior="scroll" direction="left" scrollamount="10" style="font-size:24px; color:black;">
            This Dashboard Provides Various Tools to Visualize and Predict Customer Bank Churn
        </marquee>
    """, unsafe_allow_html=True)

    # Menambahkan gambar di bawah teks marquee tanpa efek
    st.image("bank.jpg", use_column_width=True)  
# Kondisi jika pengguna memilih Visualisasi
# If the user selects Visualization
elif selected == "Visualization":
    with st.expander("Pilih Jenis Plot", expanded=True):
        # Dropdown for selecting graph type
        graph_type = st.selectbox(
            "Choose a graph type", 
            ["Histogram", "Scatter Plot", "Box Plot", "Bar Chart"]
        )

    # Applying the custom class to the title
    st.markdown('<h1 class="centered-title">Data Visualization</h1>', unsafe_allow_html=True)

    # Berdasarkan pilihan grafik, opsi untuk memilih fitur akan muncul
    if graph_type == "Histogram":
        fitur_histogram = st.selectbox('Fitur untuk Histogram', data.columns)
        if st.button('Tampilkan Histogram'):
            fig, ax = plt.subplots()
            plt.hist(data[fitur_histogram], bins=20, color='blue', edgecolor='black')
            plt.title(f'Histogram of {fitur_histogram}')
            plt.xlabel(fitur_histogram)
            plt.ylabel('Frequency')
            st.pyplot(fig)

    elif graph_type == "Scatter Plot":
        x_axis = st.selectbox('Fitur untuk X-Axis', data.columns, key='x_axis')
        y_axis = st.selectbox('Fitur untuk Y-Axis', data.columns, key='y_axis')
        if st.button('Tampilkan Scatter Plot'):
            fig, ax = plt.subplots()
            sns.scatterplot(x=data[x_axis], y=data[y_axis])
            plt.title(f'Scatter Plot of {x_axis} vs {y_axis}')
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            st.pyplot(fig)

    elif graph_type == "Box Plot":
        fitur_boxplot = st.selectbox('Fitur untuk Box Plot', data.columns)
        if st.button('Tampilkan Box Plot'):
            fig, ax = plt.subplots()
            sns.boxplot(data=data[fitur_boxplot])
            plt.title(f'Box Plot of {fitur_boxplot}')
            st.pyplot(fig)
                    # Bar chart hanya untuk fitur HasCrCard dan IsActiveMember
    elif graph_type == "Bar Chart":
        fitur_bar = st.selectbox('Fitur untuk Bar Chart', ['HasCrCard', 'IsActiveMember'])
        if st.button('Tampilkan Bar Chart'):
            fig, ax = plt.subplots()
            # Menghitung frekuensi tiap kategori
            data_counts = data[fitur_bar].value_counts()
            plt.bar(data_counts.index, data_counts.values, color='blue')
            plt.title(f'Bar Chart of {fitur_bar}')
            plt.xlabel(fitur_bar)
            plt.ylabel('Count')
            st.pyplot(fig)

# Kondisi jika pengguna memilih Prediksi
elif selected == "Prediction":
        
    st.markdown(
        """
        <style>
        .title-style {
            font-size: 32px;
            font-weight: bold;
            color: black;
            text-align: center;
            margin-bottom: 25px;
        }

        .stButton>button {
            background-color: grey;
            color: white;
            padding: 10px 50px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
        }

        .stButton>button:hover {
            background-color: grey;
        }

        .center-button {
            display: flex;
            justify-content: center;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Enhanced Title
    st.markdown('<h1 class="title-style">Prediction Section</h1>', unsafe_allow_html=True)


    # Input untuk prediksi# Input for numerical values with unique keys
    credit_score = st.number_input('CreditScore', min_value=0, value=0, key='credit_score')
    age = st.number_input('Age', min_value=0, value=0, key='age')
    tenure = st.number_input('Tenure', min_value=0, value=5, key='tenure')
    balance = st.number_input('Balance', min_value=0.0, value=0.0, key='balance')
    num_of_products = st.number_input('Number of Products', min_value=0, max_value=4, value=0, key='num_of_products')
    estimated_salary = st.number_input('Estimated Salary', min_value=0.0, value=0.0, key='estimated_salary')

    # Input kategori untuk Gender, Has Credit Card, dan Active Member
    gender = st.selectbox('Gender', options=['Male', 'Female'])
    has_cr_card = st.selectbox('Has Credit Card', options=['Yes', 'No'])
    is_active_member = st.selectbox('Is Active Member', options=['Yes', 'No'])

    # One-Hot Encoding untuk input kategori
    gender_female = 1 if gender == 'Female' else 0
    gender_male = 1 if gender == 'Male' else 0
    has_cr_card_yes = 1 if has_cr_card == 'Yes' else 0
    has_cr_card_no = 1 if has_cr_card == 'No' else 0
    is_active_member_yes = 1 if is_active_member == 'Yes' else 0
    is_active_member_no = 1 if is_active_member == 'No' else 0 
    # Data baru dalam dictionary
    new_data = {
        'CreditScore': [credit_score],
        'Age': [age],
        'Tenure': [tenure],
        'Balance': [balance],
        'NumOfProducts': [num_of_products],
        'EstimatedSalary': [estimated_salary],
        'Gender': [gender],
        'HasCrCard': [has_cr_card],
        'IsActiveMember': [is_active_member]
    }

    # Ubah data baru menjadi DataFrame
    new_data_df = pd.DataFrame(new_data)

    st.markdown('<div class="center-button">', unsafe_allow_html=True)  # Open div for centering
    if st.button('Prediksi', key='prediction_button'):
        # Preprocess new data
        new_data_processed = preprocess_input_data(new_data_df, columns_after_encoding)

        # Prediction
        new_data_tensor = torch.tensor(new_data_processed, dtype=torch.float32)
        model.eval()  # Set model to evaluation mode
        with torch.no_grad():
            output = model(new_data_tensor)
            prediction = (output > 0.5).float()
            
            # Menambahkan custom font dan ukuran
            if int(prediction.item()) == 1:
                st.markdown(
                    "<h1 style='font-family:sans-serif; font-size:36px; color:red;'>"
                    "⚠️ Prediksi: Churn"
                    "</h1>", unsafe_allow_html=True)
            else:
                st.markdown(
                    "<h1 style='font-family:sans-serif; font-size:36px; color:green;'>"
                    "✅ Prediksi: Not Churn"
                    "</h1>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close div for centering
 
