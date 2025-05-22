def process_uploaded_file(file_obj, file_name):
    import pandas as pd
    import numpy as np
    import io
    from connections import connection_pos

    customer_master = pd.read_sql("""
        SELECT customer_code, mobile_number FROM customers
    """, connection_pos())
    customer_master['mobile_number_91'] = '91' + customer_master['mobile_number'].astype(str)
    customer_master = customer_master[['mobile_number_91', 'customer_code']]
    customer_master.columns = customer_master.columns.str.lower()

    file_ext = file_name.split(".")[-1].lower()
    output = io.BytesIO()

    try:
        if file_ext == "csv":
            df = pd.read_csv(file_obj)
            df.columns = df.columns.str.lower()
            if 'mobile number' in df.columns:
                df['mobile number'] = df['mobile number'].astype(str).apply(lambda x: x.split('.')[0])
                df = df.merge(customer_master, how='left', left_on='mobile number', right_on='mobile_number_91')
                drop_cols = ['mobile_number_91', 'name', 'mobile number']

                df = df.drop(columns=[col for col in drop_cols if col in df.columns])
            df.to_csv(output, index=False)
            output.seek(0)
            return output, file_name, "text/csv"

        elif file_ext in ["xls", "xlsx"]:
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            all_sheets = pd.read_excel(file_obj, sheet_name=None)

            for sheet_name, df in all_sheets.items():
                if df.shape[0] > 0:
                    df[df.columns] = df[df.columns].astype(str)
                    df.columns = df.columns.str.lower()
                    if 'mobile number' in df.columns:
                        df['mobile number'] = df['mobile number'].astype(str).apply(lambda x: x.split('.')[0])
                        df = df.merge(customer_master, how='left', left_on='mobile number', right_on='mobile_number_91')
                        drop_cols = ['mobile_number_91', 'name', 'mobile number']
                        df = df.drop(columns=[col for col in drop_cols if col in df.columns])
                    df = df.replace('nan', np.nan)
                df.to_excel(writer, sheet_name=sheet_name, index=False)

            writer.close()
            output.seek(0)
            return output, file_name, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        else:
            raise ValueError("Unsupported file type.")

    except Exception as e:
        raise RuntimeError(f"Processing failed: {e}")
