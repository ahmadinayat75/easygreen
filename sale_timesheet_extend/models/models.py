# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectOverview(models.Model):
    _inherit = 'project.project'

    def _plan_prepare_values(self):
        values = super()._plan_prepare_values()
        project_cost = 0
        rec_task = self.env['project.task'].search([('project_id', 'in', self.ids)])
        for rec_moves in rec_task.stock_move_ids:
            move_lines = self.env['account.move'].search([('stock_move_id', 'in', rec_moves.ids)])
            project_cost += sum(project_costs.amount_total_signed for project_costs in move_lines)
            project_cost = round(project_cost, 2)
        income_list = self.env['profit.loss.type'].search([('sign', '=', '+')])
        income_vals = []
        income_amount = []
        for rec_type in income_list:
            type_title = rec_type.name
            charts_list = self.env['account.account'].search([('profit_type','=',rec_type.id)])
            journal_items = self.env['account.move.line'].search(
                [('analytic_account_id', 'in', self.analytic_account_id.ids), ('account_id','in',charts_list.ids)])
            journal_debit = sum(journal_vals.debit for journal_vals in journal_items)
            journal_credit = sum(journal_vals.credit for journal_vals in journal_items)
            final_amount = journal_credit - journal_debit
            income_vals.append({'vals': final_amount, 'title': type_title})
            income_amount.append(final_amount)
        income_list = self.env['profit.loss.type'].search([('sign', '=', '-')])
        expense_vals = []
        expense_amount = []
        for rec_type in income_list:
            expense_titles = rec_type.name
            charts_list = self.env['account.account'].search([('profit_type', '=', rec_type.id)])
            journal_items = self.env['account.move.line'].search(
                [('analytic_account_id', 'in', self.analytic_account_id.ids), ('account_id', 'in', charts_list.ids)])
            journal_debit = sum(journal_vals.debit for journal_vals in journal_items)
            journal_credit = sum(journal_vals.credit for journal_vals in journal_items)
            final_expense = journal_debit - journal_credit
            final_expense = - final_expense
            expense_vals.append({'vals':final_expense,
                                 'title':expense_titles})
            expense_amount.append(final_expense)

        sum_exp = sum(expense_amount)
        sum_income = sum(income_amount)
        net_income = sum_income + sum_exp
        values.update({'income_vals': income_vals,'expense_vals': expense_vals, 'sum_exp':sum_exp, 'sum_income': sum_income, 'net_income' : net_income})
        return values


class ProfitLossType(models.Model):
    _name = 'profit.loss.type'

    name = fields.Char('Description')
    type = fields.Selection([("income", "Income"), ("expense", "Expense")], string="Type")
    sign = fields.Char(string="Sign")

    @api.depends('type')
    @api.onchange('type')
    def onchange_account_type(self):
        for rec in self:
            if rec.type == 'income':
                rec.sign = '+'
            else:
                rec.sign = '-'


class AccountAccount(models.Model):
    _inherit = 'account.account'

    profit_type = fields.Many2one('profit.loss.type')
    internal_group = fields.Char(compute="onchange_user_id")

    @api.onchange('user_type_id')
    def onchange_user_id(self):
        for rec in self:
            rec.internal_group = rec.user_type_id.internal_group

    @api.onchange('user_type_id')
    @api.depends('user_type_id')
    def _onchange_profit_type(self):
        if self.user_type_id.internal_group == 'income':
            return {'domain': {'profit_type': [('type', '=', 'income')]}}
        else:
            return {'domain': {'profit_type': [('type', '=', 'expense')]}}

