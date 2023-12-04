import streamlit as st
from sqlalchemy import text

list_jenis_kelamin = ['', 'Perempuan', 'Laki-laki'] 

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://famitawibi20:y2abk9QcReHn@ep-patient-field-58242561.us-east-2.aws.neon.tech/web?options=endpoint%3Dep-patient-field-58242561")

st.header('DATABASE SEBARAN ALUMNI MAHASISWA STATISTIKA BISNIS')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM sebaran_pekerjaan ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO sebaran_pekerjaan (nama_mahasiswa, nrp_mahasiswa, jenis_kelamin, angkatan, alamat_domisili, email, handphone, sosmed, nama_instansi, jabatan, alamat_instansi)\
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11);')
            session.execute(query, {'1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': '', '8': ' ', '9': '', '10': ' ', '11': ''})
            session.commit()

    data = conn.query('SELECT * FROM sebaran_pekerjaan ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        nama_mahasiswa_lama = result["nama_mahasiswa"]
        nrp_mahasiswa_lama = result["nrp_mahasiswa"]
        jenis_kelamin_lama = result["jenis_kelamin"]
        angkatan_lama = result["angkatan"]
        alamat_domisili_lama = result["alamat_domisili"]
        email_lama = result["email"]
        handphone_lama = result["handphone"]
        sosmed_lama = result["sosmed"]
        nama_instansi_lama = result["nama_instansi"]
        jabatan_lama = result["jabatan"]
        alamat_instansi_lama = result["alamat_instansi"]

        with st.expander(f'a.n. {nama_mahasiswa_lama}'):
            with st.form(f'data-{id}'):
                nama_mahasiswa_baru = st.text_input("nama_mahasiswa", nama_mahasiswa_lama)
                nrp_mahasiswa_baru = st.text_input("nrp_mahasiswa", nrp_mahasiswa_lama)
                jenis_kelamin_baru = st.selectbox("jenis_kelamin", list_jenis_kelamin, list_jenis_kelamin.index(jenis_kelamin_lama))
                angkatan_baru = st.text_input("angkatan", angkatan_lama)
                alamat_domisili_baru = st.text_input("alamat_domisili", alamat_domisili_lama)
                email_baru = st.text_input("email", email_lama)
                handphone_baru = st.text_input("handphone", handphone_lama)
                sosmed_baru = st.text_input("sosmed", sosmed_lama)
                nama_instansi_baru = st.text_input("nama_instansi", nama_instansi_lama)
                jabatan_baru = st.text_input("jabatan", jabatan_lama)
                alamat_instansi_baru = st.text_input("alamat_instansi", alamat_instansi_lama)

                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE sebaran_pekerjaan\
                                          SET nama_mahasiswa=:1, nrp_mahasiswa=:2, jenis_kelamin=:3, angkatan=:4, \
                                          alamat_domisili=:5, email=:6, handphone=:7, sosmed=:8 , nama_instansi=:9,  jabatan=:10, alamat_instansi=:11 \
                                          WHERE id=:12;')
                            session.execute(query, {'1':nama_mahasiswa_baru, '2':nrp_mahasiswa_baru, '3':jenis_kelamin_baru, '4':angkatan_baru, 
                                                    '5':alamat_domisili_baru, '6':email_baru, '7':handphone_baru, '8':sosmed_baru, '9':nama_instansi_baru, '10': jabatan_baru, '11':alamat_instansi_baru, '12':id})
                            session.commit()
                            st.rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        with conn.session as session:
                            query = text(f'DELETE FROM sebaran_pekerjaan WHERE id=:1')
                            session.execute(query, {'1':id})
                            session.commit()
                            st.rerun()