export interface taskI {
    id: number;
    type: string;
    userid: string;
    input: string;
    output: string;
    state: string;
    message: string;
    created_at: string;
    updated_at: string;
}

export interface filterI {
    text: string;
    value: string;
}

export interface userI {
    userid: string;
    company_name: string;
    group_name?: string;
    is_admin: boolean;
    uscid: string;
    dsj_username: string;
    dsj_password: string;
    bank_name: string;
    bank_id: string;
    staff_record?: any[];
    is_zero: boolean;
    is_bill: boolean;
    puppet_id?: string;
    invoice_habit?: string;
    create_time?: string;
    update_time?: string;
    enable: boolean;
}




